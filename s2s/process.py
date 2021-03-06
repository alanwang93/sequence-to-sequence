#!/usr/bin/env python
# coding=utf-8

import argparse
import os

from multiprocessing import Process
import s2s.datasets as datasets
from s2s.utils.vocab import Vocab

def main(args):

    dc = getattr(datasets, args.config)(args.raw_root, args.data_root)

    # Vocab files are under model path
    if args.vocab:
        print('Building vocab')
        if dc.share_vocab:
            vocab = Vocab(path=dc.path, max_vocab=dc.max_src_vocab, \
                    min_freq=dc.min_freq, unk_token=dc.unk_token)
            vocab._init_vocab()
            src_file = '{0}.{1}'.format(dc.train_prefix, dc.src)
            tgt_file = '{0}.{1}'.format(dc.train_prefix, dc.tgt)
            corpus = dc.build_corpus(src_file)
            corpus.extend(dc.build_corpus(tgt_file))
            vocab.update(corpus)
            vocab._finish()
            vocab.summary()
        else:
            src_vocab = Vocab(path=dc.path, max_vocab=dc.max_src_vocab, \
                    min_freq=dc.min_freq, prefix='src', unk_token=dc.unk_token)
            tgt_vocab = Vocab(path=dc.path, max_vocab=dc.max_tgt_vocab, \
                    min_freq=dc.min_freq, prefix='tgt', unk_token=dc.unk_token)
            src_file = '{0}.{1}'.format(os.path.join(dc.raw, dc.train_prefix), dc.src)
            tgt_file = '{0}.{1}'.format(os.path.join(dc.raw, dc.train_prefix), dc.tgt)
            src_corpus = dc.build_corpus(src_file)
            tgt_corpus = dc.build_corpus(tgt_file)
            src_vocab.build(rebuild=True, data=src_corpus)
            tgt_vocab.build(rebuild=True, data=tgt_corpus)
            src_vocab.summary()
            tgt_vocab.summary()

    else:
        print('Loading vocab')
        if dc.share_vocab:
            vocab = Vocab(path=dc.path, max_vocab=dc.max_src_vocab, \
                    min_freq=dc.min_freq, unk_token=dc.unk_token)
            vocab.build(rebuild=False)
        else:
            src_vocab = Vocab(path=dc.path, max_vocab=dc.max_src_vocab, \
                    min_freq=dc.min_freq, prefix='src', unk_token=dc.unk_token)
            src_vocab.build(rebuild=False)
            tgt_vocab = Vocab(path=dc.path, max_vocab=dc.max_tgt_vocab, \
                    min_freq=dc.min_freq, prefix='tgt', unk_token=dc.unk_token)
            tgt_vocab.build(rebuild=False)

    # if args.extract:
    #     pass
    #     for (src, tgt) in [(dc.train_src, dc.train_tgt), \
    #             (dc.valid_src, dc.valid_tgt), (dc.test_src, dc.test_tgt)]:
    #         print("Build {0}, {1}".format(src, tgt))
    #         dc.build_data(src, tgt, vocab)
        
        #file_list = dc.train_list + dc.valid_list + dc.test_list
        #processes = [Process(target=dc.extract, args=(f, vocab)) for f in file_list]
        #for p in processes:
        #    p.start()
        #for p in processes:
        #    p.join()




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=None, help='data config name')
    parser.add_argument('--vocab', dest='vocab', action='store_true', \
            help='(Re)build vocabulary')
    # parser.add_argument('--embed', dest='embed', action='store_true')
    parser.add_argument('--extract', dest='extract', action='store_true')
    parser.add_argument('--model_root', type=str, default='checkpoints')
    parser.add_argument('--data_root', type=str, default='data')
    parser.add_argument('--raw_root', type=str, default='raw')

    args = parser.parse_args()
    main(args)




