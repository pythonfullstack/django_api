import random
import string
import sys

from django.conf import settings

sys.path.append('hifi-gan')
sys.path.append('tacotron2')
import numpy as np
import torch
import json
from hparams import create_hparams
from model import Tacotron2
from text import text_to_sequence
from env import AttrDict
from meldataset import MAX_WAV_VALUE
from models import Generator
import os

import tensorflow as tf

tf.compat.v1
from scipy.io.wavfile import write


def inference(text, model_path):
    print(text, model_path)
    thisdict = {}
    for line in reversed((open('./api/cloning/merged.dict.txt', "r").read()).splitlines()):
        thisdict[(line.split(" ", 1))[0]] = (line.split(" ", 1))[1].strip()

    def ARPA(text, punctuation=r"!?,.;", EOS_Token=True):
        out = ''
        for word_ in text.split(" "):
            word = word_
            end_chars = ''
            while any(elem in word for elem in punctuation) and len(word) > 1:
                if word[-1] in punctuation:
                    end_chars = word[-1] + end_chars
                    word = word[:-1]
                else:
                    break
            try:
                word_arpa = thisdict[word.upper()]
                word = "{" + str(word_arpa) + "}"
            except KeyError:
                pass
            out = (out + " " + word + end_chars).strip()
        if EOS_Token and out[-1] != ";": out += ";"
        return out

    def get_hifigan():
        # Download HiFi-GAN
        hifigan_pretrained_model = os.path.join(settings.MEDIA_ROOT, 'hifi_model')

        # Load HiFi-GAN
        conf = os.path.join("hifi-gan", "config_v1.json")
        with open(conf) as f:
            json_config = json.loads(f.read())
        h = AttrDict(json_config)
        torch.manual_seed(h.seed)
        hifigan = Generator(h).to(torch.device("cuda"))
        state_dict_g = torch.load(hifigan_pretrained_model, map_location=torch.device("cuda"))
        hifigan.load_state_dict(state_dict_g["generator"])
        hifigan.eval()
        hifigan.remove_weight_norm()
        return hifigan, h

    hifigan, h = get_hifigan()
    print("reading 1")

    def has_MMI(STATE_DICT):
        return any(True for x in STATE_DICT.keys() if "mi." in x)

    def get_Tactron2():
        # Load Tacotron2 and Config
        hparams = create_hparams()
        hparams.sampling_rate = 22050
        hparams.max_decoder_steps = 3000  # Max Duration
        hparams.gate_threshold = 0.25  # Model must be 25% sure the clip is over before ending generation
        model = Tacotron2(hparams)
        state_dict = torch.load(model_path)['state_dict']
        if has_MMI(state_dict):
            raise Exception("ERROR: This notebook does not currently support MMI models.")
        model.load_state_dict(state_dict)
        _ = model.cuda().eval().half()
        return model, hparams

    # Extra Info
    def end_to_end_infer(pronounciation_dictionary):
        for i in [x for x in text.split("\n") if len(x)]:
            if not pronounciation_dictionary:
                if i[-1] != ";": i = i + ";"
            else:
                i = ARPA(i)
            with torch.no_grad():  # save VRAM by not including gradients
                sequence = np.array(text_to_sequence(i, ['english_cleaners']))[None, :]
                sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()
                mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
                y_g_hat = hifigan(mel_outputs_postnet.float())
                audio = y_g_hat.squeeze()
                audio = audio * MAX_WAV_VALUE

                # ipd.display(ipd.Audio(audio.cpu().numpy().astype("int16"), rate=hparams.sampling_rate))
                rnd_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
                write(f'{rnd_string}.wav', hparams.sampling_rate, audio.cpu().numpy().astype("int16"))
                print("reading 2")
                return rnd_string

    model, hparams = get_Tactron2()

    pronounciation_dictionary = False  # @param {type:"boolean"}
    # disables automatic ARPAbet conversion, useful for inputting your own ARPAbet pronounciations or just for testing
    model.decoder.max_decoder_steps = 1000  # @param {type:"integer"}
    stop_threshold = 0.324  # @param {type:"number"}
    model.decoder.gate_threshold = stop_threshold

    end_to_end_infer(pronounciation_dictionary)
