# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: February, 16, 2019
# Title:HackNYU Emotion2Paint

# This application/product/tool makes use of the <resource name>, created by <author(s)> at the National Research Council Canada." (The creators of each lexicon are listed below. Also, if you send us an email, we will be thrilled to know about how you have used the lexicon.) If possible hyperlink to this page: http://saifmohammad.com/WebPages/lexicons.html

import pickle
import os
import random

class Emotion2Art:
    """Map emotional string to paint url."""

    

    def __init__(self, n_rst = 0):
        """
        initialize an transform object. If imgs haven't been mapped to
        quadrants, map them and serialized them into a pickle file, saved under
        the same directory. Else, load from pickle file.

        Args:
            word (str): The string that's passed in to match emotion.
            n_rst (int): Choose randomly from n closest paints, return one of 
            them.
        
        Returns:
            none.
        """
        tsv_src = "WikiArt-Emotions/WikiArt-Emotions/WikiArt-Emotions-Ag4.tsv" # Location of mapping file.
        self.n_rst = n_rst
        if not os.path.exists("img_quadrant.pkl"):
            img_drct = self._mapping(tsv_src) # map 
            with open("img_quadrant.pkl", "wb") as fout:
                pickle.dump(img_drct,fout)
                fout.close()
            # save data to pickle file
        with open("img_quadrant.pkl", "rb") as fin:
                self.img_qdrt = pickle.load(fin) 
            # save img quadrant in self.img
                fin.close()

    def _mapping(self, tsv):
        """
            map emotions with vectors, use coefficients to determine where the 
            paintings belong to.

            Args:
                tsv (str): The directory of the dataset 
            
            Returns:
                retval (dict): return value is the dictionary of each quadrant,
                where the items are lists of img info.
        """ 

        # d_emo_direct = { 
        # # word sentiment in valence,arousal
        # # neutral being 0.5, 0.5 
        #     "agreeableness" : [0.5, 0.5], 
        #     "anger" : [0.167,0.865],
        #     "anticipation" : [0.4,0.4], 
        #     "arrogance" : [0.8, -0.8], 
        #     "disagreeableness" : [0.5, 0.5], 
        #     "disgust" : [0.5, -0.5], 
        #     "fear" : [0.1, 0.1], 
        #     "gratitude" : [0.885, 0.441], 
        #     "happiness" : [0.960, 0.732], 
        #     "humility" : [0.7440,0.118], 
        #     "love" : [1.000,0.519], 
        #     "optimism" : [0.949, 0.565], 
        #     "pessimism" : [0.083, 0.484], 
        #     "regret" : [0.230, 0.623], 
        #     "sadness" : [0.052, 0.288], 
        #     "shame" : [0.060, 0.670], 
        #     "shyness" : [0.312, 0.265], 
        #     "surprise" : [0.875, 0.875], 
        #     "trust" : [0.888, 0.547], 
        #     "neutral" : [0.5,0.5] 
        # }

        l_emo_direct = [[0.5, 0.5], # agreeableness
                        [0.167,0.865], # anger
                        [0.4,0.4],  # anticipation
                        [0.8, -0.8],  # arrogance
                        [0.5, 0.5],  # disagreeableness
                        [0.5, -0.5], # disgust 
                        [0.1, 0.1],  # fear
                        [0.885, 0.441], # gratitude
                        [0.960, 0.732], # happiness
                        [0.7440,0.118], # humility
                        [1.000,0.519],  # love
                        [0.949, 0.565], # optimism
                        [0.083, 0.484], # pessimism
                        [0.230, 0.623], # regret
                        [0.052, 0.288], # sadness
                        [0.060, 0.670], # shame
                        [0.312, 0.265], # shyness
                        [0.875, 0.875], # surprise
                        [0.888, 0.547], # trust
                        [0.5,0.5]  # neutral
                        ]

        retval = {
            "Q1":[],
            "Q2":[],
            "Q3":[],
            "Q4":[]
        }
        # list of indicating values for VAD emotion chart
        with open(tsv, 'r') as fin:
            meta = fin.readlines()

            cnt = 0 # count the number of images
            for ptline in meta:
                if cnt == 0:
                    cnt += 1
                    print(ptline.split('\t'))
                    continue
                # style, category, artist, title, year, imgurl]
                pt = ptline.split('\t')
                content = [pt[1],pt[2],pt[3],pt[4],pt[5],pt[6]]
                va, ar = sum([int(pt[i])*l_emo_direct[i-32][0] for i in range(32,52)]),\
                    sum([int(pt[i])*l_emo_direct[i-32][1] for i in range(32,52)])
                        # compute direct quadrant (valerance, arousal)
                # assign 1, 2, 3, 4 as four different quadrants

                if va >= 0.5:
                    if ar >= 0.5:
                        retval["Q1"].append(content)
                    else:
                        retval["Q2"].append(content)
                else:
                    if ar >= 0.5:
                        retval["Q3"].append(content)
                    else:
                        retval["Q4"].append(content)
            return retval
        
    def match_paint(self, qd):
        """
            randomly returns a list of the info of a img in the 
            matching quadrant.

            Args:
                qd(int): the quadrant of the music piece  
            
            Returns:
                url(str): the url of the chosen image
        """

        return random.choice(self.img_qdrt["Q{}".format(qd)])[-1]

if __name__ == "__main__":
    a = Emotion2Art()
    print(a.match_paint(1))

