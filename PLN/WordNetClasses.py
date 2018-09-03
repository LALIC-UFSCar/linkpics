from nltk.corpus import wordnet as wn
'''
lst = wn.synsets('motorbike', pos=wn.NOUN)
hyper = lambda s: s.hypernyms()
for j in range(0, len(lst)):
        synset = str(lst[j])
        synset = synset.replace("Synset('", "")
        synset = synset.replace("')", "")
        print(synset + " ----" + wn.synset(synset).definition())
        '''
'''



hyper = lambda s: s.hypernyms()

#'location.n.01' side


person= wn.synset('country.n.04')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))


person= wn.synset('nation.n.02')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))

person= wn.synset('area.n.01')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))


person= wn.synset('landscape.n.01')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))

person= wn.synset('landscape.n.02')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))


person= wn.synset('landscape.n.03')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))

person= wn.synset('landscape.n.04')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))

'''

word_1 = wn.synset('lion.n.01')
word_2 = wn.synset('dog.n.01')
distancia_wup = word_1.wup_similarity(word_2)
#print('distancia wup: ' + str(distancia_wup))


def TrazerSynsetBoundingBox(palavra):

    if palavra == 'motorbike':
        motorbike = wn.synset('minibike.n.01 ')
        return motorbike
    if palavra == 'bicycle':
        bicycle = wn.synset('bicycle.n.01 ')
        return bicycle
    if palavra == 'car':
        car = wn.synset('car.n.01')
        return car

    if palavra == 'aeroplane':
        aeroplane = wn.synset('airplane.n.01')
        return aeroplane

    if palavra == 'bus':
        bus = wn.synset('bus.n.01')
        return bus

    if palavra == 'train':
        train = wn.synset('train.n.01')
        return train

    if palavra == 'truck':
        truck = wn.synset('truck.n.01')
        return truck

    if palavra == 'boat':
        boat = wn.synset('boat.n.01')
        return boat

    if palavra == 'semaphore':
        traffic_light = wn.synset('light.n.02')
        return traffic_light

    if palavra == 'hydrant':
        fire_hydrant = wn.synset('water_faucet.n.01')
        return fire_hydrant

    if palavra == 'stop':
        stop_sign = wn.synset('signboard.n.01 ')
        return stop_sign

    if palavra == 'parking':
        parking_meter = wn.synset('parking.n.01 ')
        return parking_meter

    if palavra == 'bench':
        bench = wn.synset('bench.n.01')
        return bench

    if palavra == 'bird':
        bird = wn.synset('bird.n.01')
        return bird

    if palavra == 'cat':
        cat = wn.synset('cat.n.01')
        return cat

    if palavra == 'dog':
        dog = wn.synset('dog.n.01')
        return dog

    if palavra == 'horse':
        horse = wn.synset('horse.n.01')
        return horse

    if palavra == 'sheep':
        sheep = wn.synset('sheep.n.01')
        return sheep

    if palavra == 'cow':
        cow = wn.synset('cow.n.01')
        return cow

    if palavra == 'elephant':
        elephant = wn.synset('elephant.n.0')
        return elephant

    if palavra == 'bear':
        bear = wn.synset('bear.n.01')
        return bear

    if palavra == 'zebra':
        zebra = wn.synset('zebra.n.01')
        return zebra

    if palavra == 'giraffe':
        giraffe = wn.synset('giraffe.n.01')
        return giraffe

    if palavra == 'backpack':
        backpack = wn.synset('backpack.n.01')
        return backpack

    if palavra == 'umbrella':
        umbrella = wn.synset('umbrella.n.01')
        return umbrella

    if palavra == 'handbag':
        handbag = wn.synset('bag.n.04')
        return handbag

    if palavra == 'tie':
        tie = wn.synset('necktie.n.01')
        return tie

    if palavra == 'suitcase':
        suitcase = wn.synset('bag.n.06')
        return suitcase

    if palavra == 'frisbee':
        frisbee = wn.synset('frisbee.n.01')
        return frisbee

    if palavra == 'skis':
        skis = wn.synset('ski.n.01')
        return skis

    if palavra == 'snowboard':
        snowboard = wn.synset('snowboard.n.01')
        return snowboard

    if palavra == 'ball':
        ball = wn.synset('ball.n.01 ')
        return ball

    if palavra == 'kite':
        kite = wn.synset('kite.n.03')
        return kite

    if palavra == 'stick':
        baseball_bat = wn.synset('stick.n.01')
        return baseball_bat

    if palavra == 'glove':
        baseball_glove = wn.synset('baseball_glove.n.01')
        return baseball_glove

    if palavra == 'skateboard':
        skateboard = wn.synset('skateboard.n.01')
        return skateboard

    if palavra == 'surfboard':
        surfboard = wn.synset('surfboard.n.01')
        return surfboard

    if palavra == 'racket':
        racket = wn.synset('racket.n.04')
        return racket

    if palavra == 'bottle':
        bottle = wn.synset('bottle.n.01')
        return bottle

    if palavra == 'glass':
        glass = wn.synset('glass.n.02')
        return glass

    if palavra == 'cup':
        cup = wn.synset('cup.n.01')
        return cup

    if palavra == 'fork':
        fork = wn.synset('fork.n.01')
        return fork

    if palavra == 'knife':
        knife = wn.synset('knife.n.01')
        return knife
    if palavra == 'spoon':
        spoon = wn.synset('spoon.n.01')
        return spoon

    if palavra == 'bowl':
        bowl = wn.synset('bowl.n.01')
        return bowl

    if palavra == 'banana':
        banana = wn.synset('banana.n.01')
        return banana

    if palavra == 'sandwich':
        sandwich = wn.synset('sandwich.n.01')
        return sandwich

    if palavra == 'orange':
        orange = wn.synset('orange.n.01')
        return orange

    if palavra == 'broccoli':
        broccoli = wn.synset('broccoli.n.01')
        return broccoli

    if palavra == 'carrot':
        carrot = wn.synset('carrot.n.01')
        return carrot

    if palavra == 'sausage':
        hot_dog = wn.synset('frank.n.02')
        return hot_dog

    if palavra == 'pizza':
        pizza = wn.synset('pizza.n.01')
        return pizza

    if palavra == 'donut':
        donut = wn.synset('doughnut.n.02')
        return donut

    if palavra == 'cake':
        cake = wn.synset('cake.n.03')
        return cake

    if palavra == 'chair':
        chair = wn.synset('chair.n.01')
        return chair

    if palavra == 'sofa':
        sofa = wn.synset('sofa.n.01')
        return sofa

    if palavra == 'vase':
        pottedplant = wn.synset('vase.n.01')
        return pottedplant

    if palavra == 'bed':
        bed = wn.synset('bed.n.01')
        return bed

    if palavra == 'table':
        dinningtable = wn.synset('table.n.02')
        return dinningtable

    if palavra == 'toilet':
        toilet = wn.synset('toilet.n.02')
        return toilet

    if palavra == 'monitor':
        tvmonitor = wn.synset('monitor.n.04')
        return tvmonitor

    if palavra == 'laptop':
        laptop = wn.synset('laptop.n.01')
        return laptop

    if palavra == 'mouse':
        mouse = wn.synset('mouse.n.04')
        return mouse

    if palavra == 'remote control':
        remote = wn.synset('remote_control.n.01')
        return remote

    if palavra == 'keyboard':
        keyboard = wn.synset('keyboard.n.01')
        return keyboard

    if palavra == 'phone':
        cell = wn.synset('cellular_telephone.n.01')
        return cell

    if palavra == 'microwave':
        microwave = wn.synset('microwave.n.02')
        return microwave

    if palavra == 'oven':
        oven = wn.synset('oven.n.01')
        return oven
    if palavra == 'toaster':
        toaster = wn.synset('toaster.n.02')
        return toaster

    if palavra == 'sink':
        sink = wn.synset('sink.n.01')
        return sink

    if palavra == 'refrigerator':
        refrigerator = wn.synset('refrigerator.n.01')
        return refrigerator

    if palavra == 'book':
        book = wn.synset('book.n.01')
        return book

    if palavra == 'clock':
        clock = wn.synset('clock.n.01')
        return clock

    if palavra == 'vase':
        vase = wn.synset('vase.n.01')
        return vase

    if palavra == 'scissors':
        scissors = wn.synset('scissors.n.01')
        return scissors

    if palavra == 'plush':
        teddy = wn.synset('teddy.n.01')
        return teddy

    if palavra == 'dryer':
        drier = wn.synset('dryer.n.01')
        return drier

    if palavra == 'toothbrush':
        toothbrush = wn.synset('toothbrush.n.01')
        return toothbrush

    #print(person.wup_similarity(phone))
