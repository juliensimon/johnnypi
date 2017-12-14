import numpy as np
import mxnet as mx
import cv2, time
from collections import namedtuple

def load_inception_model():
    with open('./synset.txt', 'r') as f:
        synsets = [l.rstrip() for l in f]
    sym, arg_params, aux_params = mx.model.load_checkpoint('Inception-BN', 0)
    model = mx.mod.Module(symbol=sym, context=mx.cpu())
    model.bind(for_training=False, data_shapes=[('data', (1,3,224,224))])
    model.set_params(arg_params, aux_params)
    return model,synsets
 
def load_image(filename):
    img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img

def get_top_categories(prob, n=5):
    topN = []
    a = np.argsort(prob)[::-1]
    for i in a[0:n]:
        print('probability=%f, class=%s' %(prob[i], synsets[i]))
        topN.append((prob[i], synsets[i]))
    return topN

def build_top1_message(topN):
    top1 = topN[0]
    # Convert probability to integer percentage
    prob = (str)((int)(top1[0]*100))
    # Remove category number
    item = top1[1].split(' ')
    item = ' '.join(item[1:])
    message = "I'm "+prob+"% sure that this is a "+item+". "
    return message
    
def predict(image, model):
    Batch = namedtuple('Batch', ['data'])
    time1 = time.time()
    model.forward(Batch([mx.nd.array(image)]))
    prob = model.get_outputs()[0].asnumpy()
    prob = np.squeeze(prob)
    time2 = time.time()
    print "forward pass in "+str(time2-time1)
    return prob

