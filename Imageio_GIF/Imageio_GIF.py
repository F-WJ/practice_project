__author__  =  'FWJ' 
__time__  =  '2018-11-11 10:45:05' 
from create_gif import create
import os

def main():
    filepath = './ins'
    image_list = os.listdir(filepath)
    git_name = 'new.gif'
    duration = 1
    os.chdir('./ins')
    create(image_list, git_name)


if __name__ == "__main__":
    # main()
    main()
   
