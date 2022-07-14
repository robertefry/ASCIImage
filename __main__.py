
##     _    ____   ____ ___ ___   ___
##    / \  / ___| / ___|_ _|_ _| |_ _|_ __ ___   __ _  __ _  ___
##   / _ \ \___ \| |    | | | |   | || '_ ` _ \ / _` |/ _` |/ _ \
##  / ___ \ ___) | |___ | | | |   | || | | | | | (_| | (_| |  __/
## /_/   \_\____/ \____|___|___| |___|_| |_| |_|\__,_|\__, |\___|
##                                                    |___/
##
## A Python program to construct an image from some given text.
##
## We use the ascii table, asciimap_5x7.png`, as our character set.
##      20-2f:    ! " # $ % & ' ( ) * + , - . /
##      30-3f:  0 1 2 3 4 5 6 7 8 9 : ; < = > ?
##      40-4f:  @ A B C D E F G H I J K L M N O
##      50-5f:  P Q R S T U V Q X Y Z [ \ ] ^ _
##      60-6f:  ` a b c d e f g h i j k l m n o
##      70-7f:  p q r s t u v q x y z { | } ~
## The NUL key, 0x00, is used inplaceof an unknown character.
##

from PIL import Image
import sys

class CharMap:

    def __init__(self,charmap):
        try:
            self.image = Image.open(charmap)
        except IOError:
            sys.stderr.write("Failed to open the character map, {charmap}!\n")
            exit(-1)
        self.token_wid = int(self.image.size[0] / 16)
        self.token_hei = int(self.image.size[1] / 16)

    def decode(self,c):
        code = ord(c)
        if code < 0x20:
            code = 0x00
            print(f"[warning] unrecognised character, \'{c}\'.")
        i,j = int(code%16),int(code/16)
        return i,j

    def get(self,c):
        i,j = self.decode(c)
        w,h = self.token_wid,self.token_hei
        token = self.image.crop((i*w+1,j*h+1,(i+1)*w,(j+1)*h))
        return token

class Builder:

    def __init__(self):
        self.image = Image.new("RGB",(1,1),0xFFFFFF)
        self.x,self.y = 1,1

    def put(self,token):
        w = self.image.size[0]+token.size[0]+1
        h = max(self.image.size[1],token.size[1]+2)

        image = Image.new("RGB",(w,h),0xFFFFFF)
        image.paste(self.image)
        image.paste(token,(self.x,self.y))

        self.image = image
        self.x += token.size[0]+1

if __name__ == "__main__":

    # the string we will use to generate the resulting image
    if len(sys.argv) > 1:
        string = sys.argv[1]
    else:
        string = input("No string given as an argument. Please enter a string.\n> ")

    print(f"Generating the ASCII Image for \"{string}\"...")

    # open our character map
    charmap = CharMap("asciimap_5x7.png")
    builder = Builder()

    for c in string:
        token = charmap.get(c)
        builder.put(token)

    builder.image.show()
