import argparse
import os
import numpy as np
from scipy import io as sio
from scipy.misc import imsave

def store_img(X, y, mapping, op_folder):
    l_idx = np.zeros(62, dtype=np.int)
    for sfold in map(chr, mapping[:, 1]):
        op_fold = os.path.join(op_folder, sfold)
        if not os.path.exists(op_fold):
            os.makedirs(op_fold)

    for im, l in zip(X, y):
        l_idx[l] += 1
        l_str = chr(mapping[l, 1])
        op_f = 'img_{}_{}.png'.format(l_str, l_idx[l])
        op_fname = os.path.join(op_folder, l_str, op_f)
        imsave(name=op_fname, arr=im)

    print l_idx

   

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_matfile', type=str, required=True, 
        help='Input mat file name')
    parser.add_argument('--train_folder', type=str,
        help='The output folder name, where the train images will be stored.')
    parser.add_argument('--test_folder', type=str,
        help='The output folder name, where the test images will be stored.')
    parser.add_argument('--train_filename', type=str,
        help='Train npz file name')
    parser.add_argument('--test_filename', type=str,
        help='Test npz file name')
    parser.add_argument('--tr_fname_28', type=str,
        help='Train npz file name')
    parser.add_argument('--ts_fname_28', type=str,
        help='Test npz file name')

    args = parser.parse_args()

    print args

    mat = sio.loadmat(args.ip_matfile)
    data = mat['dataset']

    X_train = data['train'][0,0]['images'][0,0]
    y_train = data['train'][0,0]['labels'][0,0][:, 0]
    X_test = data['test'][0,0]['images'][0,0]
    y_test = data['test'][0,0]['labels'][0,0][:, 0]

    X_train_im = X_train.reshape( (X_train.shape[0], 28, 28), order='F')
    X_test_im = X_test.reshape( (X_test.shape[0], 28, 28), order='F')
    
    print 'X_train : ', X_train.shape
    print 'X_train_im : ', X_train_im.shape
    print 'X_test : ', X_test.shape
    print 'y_train : ', y_train.shape
    print 'y_test : ', y_test.shape
   
    if args.train_folder != None:
        store_img(X_train_im, y_train, data['mapping'][0, 0], args.train_folder)

    if args.test_folder != None:
        store_img(X_test_im, y_test, data['mapping'][0, 0], args.test_folder)

    if args.train_filename != None:
        X_train = np.float32(X_train) / 255.
        np.savez_compressed(args.train_filename, data=X_train, labels=y_train)
    if args.test_filename != None:
        X_test = np.float32(X_test) / 255.
        np.savez_compressed(args.test_filename, data=X_test, labels=y_test)


    if args.tr_fname_28 != None:
        X_train = np.float32(X_train_im) / 255.
        X_train = np.expand_dims(X_train, axis=-1)
        print 'X_train : ', X_train.shape
        np.savez_compressed(args.tr_fname_28, data=X_train, labels=y_train)
    if args.ts_fname_28 != None:
        X_test = np.float32(X_test_im) / 255.
        X_test = np.expand_dims(X_test, axis=-1)
        print 'X_test : ', X_test.shape
        np.savez_compressed(args.ts_fname_28, data=X_test, labels=y_test)


