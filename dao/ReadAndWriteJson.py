#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os


class IndexPageInfoDao(object):
    def __init__(self, basePath):
        self.basePath = basePath
        self.daoPath = os.path.join(self.basePath, 'repository')
        self.indexImageInfPath = os.path.join(self.daoPath, 'indexImageInf.json')
        self.detailDir = os.path.join(self.daoPath, 'detail')

    def getIndexPageImageDetailArray(self):
        loadJson = {}
        if os.path.exists(self.indexImageInfPath):
            with open(self.indexImageInfPath) as indexImageInfo:
                loadJson = json.load(indexImageInfo)

        return loadJson

    def getSpecifiedDetailInfo(self, name):
        loadJson = {}
        detailPath = os.path.join(self.detailDir, name + '.json')
        if os.path.exists(detailPath):
            with open(detailPath) as detailImfon:
                loadJson = json.load(detailImfon)

        return loadJson




if __name__ == "__main__":
    from PathConfig import basedpath
    ipid = IndexPageInfoDao(basedpath)

    print(ipid.getIndexPageImageDetailArray())