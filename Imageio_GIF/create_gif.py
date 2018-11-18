__author__  =  'FWJ' 
__time__  =  '2018-11-13 16:32:43' 
import imageio


def create(images_list, git_name, duration = 1):
    '''
    新建GIF 
    '''
    frames =[]
    for image_name in images_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(git_name, frames, 'GIF', duration = duration)

    