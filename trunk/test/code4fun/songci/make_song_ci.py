#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import random



chars = [u'\u56de', u'\u65e7', u'\u67f3', u'\u5934', u'\u51e0',
         u'\u4e0b', u'\u9ec4', u'\u6885', u'\u843d', u'\u597d', u'\u7fe0',
         u'\u65ad', u'\u884c', u'\u541b', u'\u6ee1', u'\u4e07', u'\u5357',
         u'\u4e09', u'\u591a', u'\u5728', u'\u53c8', u'\u6df1', u'\u6d41',
         u'\u77e5', u'\u697c', u'\u5c3d', u'\u89c1', u'\u524d', u'\u4e0e',
         u'\u8001', u'\u9752', u'\u6b4c', u'\u4f3c', u'\u6b64', u'\u7b11',
         u'\u91cd', u'\u4e3a', u'\u897f', u'\u770b', u'\u58f0', u'\u5c0f',
         u'\u7a7a', u'\u81ea', u'\u65b0', u'\u672a', u'\u70df', u'\u66f4',
         u'\u5fc3', u'\u6101', u'\u60c5', u'\u4e8b', u'\u4e1c', u'\u591c',
         u'\u9189', u'\u5f97', u'\u68a6', u'\u660e', u'\u79cb', u'\u98de',
         u'\u5bd2', u'\u5343', u'\u4eca', u'\u751f', u'\u91d1', u'\u91cc',
         u'\u4e2d', u'\u6c5f', u'\u957f', u'\u8c01', u'\u9152', u'\u4e0a',
         u'\u7ea2', u'\u96e8', u'\u53bb', u'\u5f52', u'\u76f8', u'\u6c34',
         u'\u6e05', u'\u5904', u'\u65e5', u'\u7389', u'\u5982', u'\u4f55',
         u'\u662f', u'\u9999', u'\u5e74', u'\u65f6', u'\u6709', u'\u5c71',
         u'\u6708', u'\u5929', u'\u6765', u'\u4e91', u'\u65e0', u'\u6625',
         u'\u4e0d', u'\u4e00', u'\u82b1', u'\u98ce', u'\u4eba']

words = [u'\u4e3a\u5bff', u'\u4e8b\u4e1a', u'\u4ead\u4ead',
         u'\u4ed9\u5bb6', u'\u4eff\u4f5b', u'\u5bab\u6bbf', u'\u5c01\u4faf',
         u'\u65e0\u5c18', u'\u6709\u4e00', u'\u6709\u9152', u'\u6e05\u5c0a',
         u'\u7389\u7bab', u'\u7559\u4f4f', u'\u7af9\u5916', u'\u7d20\u5a25',
         u'\u8537\u8587', u'\u8fdf\u8fdf', u'\u9752\u5929', u'\u98ce\u8d77',
         u'\u4f59\u9999', u'\u52cb\u4e1a', u'\u58f0\u65ad', u'\u5c0f\u6843',
         u'\u6545\u56fd', u'\u65b0\u8bd7', u'\u67f3\u4e1d', u'\u6b63\u597d',
         u'\u6d6e\u751f', u'\u70e6\u607c', u'\u8774\u8776', u'\u957f\u5578',
         u'\u4e0d\u5fcd', u'\u4f3c\u65e7', u'\u557c\u9e1f', u'\u5982\u753b',
         u'\u5a09\u5a77', u'\u6070\u4f3c', u'\u65e0\u4e8b', u'\u6726\u80e7',
         u'\u6843\u6e90', u'\u6c5f\u57ce', u'\u6c5f\u5929', u'\u767d\u5934',
         u'\u77e5\u97f3', u'\u7f57\u7eee', u'\u90fd\u4e0d', u'\u968f\u5206',
         u'\u4e00\u4efb', u'\u4e00\u5e18', u'\u4e09\u4e94', u'\u4e0d\u80af',
         u'\u4e91\u9b1f', u'\u4eba\u672a', u'\u4f73\u8282', u'\u51b5\u662f',
         u'\u662f\u5904', u'\u6709\u6068', u'\u67f3\u5916', u'\u6d1e\u5ead',
         u'\u7693\u6708', u'\u76f8\u8bc6', u'\u7ae0\u53f0', u'\u7eb1\u7a97',
         u'\u7ec6\u770b', u'\u843d\u7ea2', u'\u9189\u773c', u'\u91cd\u5e18',
         u'\u9500\u9b42', u'\u4e0d\u89c9', u'\u4e94\u66f4', u'\u4eba\u8fdc',
         u'\u4f55\u5fc5', u'\u513f\u7ae5', u'\u53e4\u6765', u'\u5c0f\u6625',
         u'\u6536\u62fe', u'\u6625\u5fc3', u'\u662f\u4e00', u'\u6de1\u70df',
         u'\u7167\u4eba', u'\u7ea4\u7ea4', u'\u82b1\u96e8', u'\u83ca\u82b1',
         u'\u897f\u7a97', u'\u91d1\u83b2', u'\u9526\u7ee3', u'\u9e67\u9e2a',
         u'\u4e9b\u513f', u'\u4eba\u8001', u'\u5230\u5982', u'\u524d\u4e8b',
         u'\u53cc\u98de', u'\u59ee\u5a25', u'\u5e74\u4eca', u'\u6885\u68a2',
         u'\u68a6\u7ed5', u'\u6b64\u6068', u'\u6e38\u4e1d', u'\u751f\u6daf',
         u'\u76f8\u5fc6', u'\u7ea2\u8896', u'\u8f7b\u76c8', u'\u4ece\u524d',
         u'\u4ece\u6559', u'\u4ed9\u4eba', u'\u5026\u5ba2', u'\u51ed\u9ad8',
         u'\u524d\u5ea6', u'\u5929\u5bd2', u'\u597d\u5904', u'\u6625\u5230',
         u'\u6b8b\u7167', u'\u6c5f\u6c34', u'\u80f8\u4e2d', u'\u83ba\u82b1',
         u'\u9001\u6625', u'\u9999\u6ee1', u'\u4e1c\u5c71', u'\u53ea\u5728',
         u'\u58f0\u91cc', u'\u5904\u662f', u'\u5ba2\u91cc', u'\u5bd2\u5bab',
         u'\u5c0a\u9152', u'\u6068\u65e0', u'\u6101\u7edd', u'\u65ad\u4e91',
         u'\u65e0\u4e00', u'\u697c\u524d', u'\u6c5f\u4e1c', u'\u6ee1\u9662',
         u'\u8c01\u4fe1', u'\u8fd8\u53c8', u'\u968f\u98ce', u'\u4e0d\u89e3',
         u'\u5439\u7bab', u'\u591a\u75c5', u'\u591c\u9611', u'\u5f97\u4f3c',
         u'\u6c34\u6676', u'\u6c88\u9999', u'\u6e05\u6d45', u'\u753b\u8239',
         u'\u9189\u5012', u'\u98ce\u8f7b', u'\u4e09\u66f4', u'\u4eba\u76f8',
         u'\u4eca\u4f55', u'\u51b0\u96ea', u'\u70df\u6811', u'\u4e2a\u4eba',
         u'\u5341\u516d', u'\u5343\u5c71', u'\u5929\u5916', u'\u5c18\u571f',
         u'\u5df2\u662f', u'\u65e0\u591a', u'\u65e7\u5bb6', u'\u6765\u53bb',
         u'\u6b22\u5a31', u'\u70df\u971e', u'\u7ecf\u5e74', u'\u81ea\u7b11',
         u'\u8bb0\u53d6', u'\u8c03\u6b4c', u'\u95ee\u4f55', u'\u964c\u4e0a',
         u'\u4eba\u5fc3', u'\u5343\u79cb', u'\u53bb\u6765', u'\u5411\u665a',
         u'\u7ea2\u53f6', u'\u82b1\u4e0d', u'\u83ab\u95ee', u'\u8c01\u5ff5',
         u'\u8e0f\u9752', u'\u8e2a\u8ff9', u'\u989c\u8272', u'\u4e0d\u8bed',
         u'\u4e1c\u6d41', u'\u4e91\u95f4', u'\u5170\u821f', u'\u5929\u6559',
         u'\u5b64\u8d1f', u'\u5b89\u6392', u'\u5c0f\u6865', u'\u5e7d\u9999',
         u'\u65e7\u4e8b', u'\u97f6\u534e', u'\u4e00\u65e5', u'\u5149\u666f',
         u'\u5c71\u5ddd', u'\u5e18\u5916', u'\u5f69\u4e91', u'\u65e0\u5b9a',
         u'\u6709\u610f', u'\u6a2a\u659c', u'\u6e56\u4e0a', u'\u773c\u524d',
         u'\u79bb\u6068', u'\u7e41\u534e', u'\u82b1\u5982', u'\u82b1\u6ee1',
         u'\u96f6\u4e71', u'\u4e00\u822c', u'\u4e34\u98ce', u'\u5347\u5e73',
         u'\u53cc\u53cc', u'\u5de5\u592b', u'\u65ad\u9b42', u'\u676f\u9152',
         u'\u6b22\u58f0', u'\u98ce\u4e0d', u'\u4e58\u5174', u'\u4eba\u6765',
         u'\u5929\u516c', u'\u5c0f\u9662', u'\u6765\u5f80', u'\u6765\u98ce',
         u'\u6de1\u6708', u'\u6e38\u620f', u'\u7389\u6811', u'\u738b\u5b59',
         u'\u8d77\u821e', u'\u9648\u8ff9', u'\u5bfb\u5e38', u'\u60f3\u89c1',
         u'\u6709\u60c5', u'\u672a\u4e86', u'\u6e05\u7edd', u'\u7409\u7483',
         u'\u76f8\u671b', u'\u770b\u770b', u'\u7eff\u7a97', u'\u83ba\u557c',
         u'\u4eba\u9053', u'\u4ed6\u5e74', u'\u4ed9\u5b50', u'\u5c81\u6708',
         u'\u60ca\u8d77', u'\u697c\u5916', u'\u6d41\u83ba', u'\u76f8\u770b',
         u'\u7ee3\u5e18', u'\u82b1\u9999', u'\u897f\u5c71', u'\u9174\u91bf',
         u'\u9898\u8bd7', u'\u513f\u5973', u'\u5904\u5904', u'\u5b64\u5c71',
         u'\u5c81\u5bd2', u'\u665a\u98ce', u'\u6b64\u65e5', u'\u79bb\u60c5',
         u'\u7a88\u7a95', u'\u80fd\u51e0', u'\u82b1\u6df1', u'\u8c01\u4e3a',
         u'\u8c01\u540c', u'\u8c2a\u4ed9', u'\u9189\u4e2d', u'\u95e8\u524d',
         u'\u4f24\u5fc3', u'\u4f9d\u7a00', u'\u5e74\u6625', u'\u6625\u886b',
         u'\u66f4\u6709', u'\u6b4c\u5934', u'\u83ab\u6559', u'\u4e00\u6bb5',
         u'\u4e24\u4e09', u'\u5c48\u6307', u'\u6101\u65e0', u'\u7559\u5f97',
         u'\u767b\u9ad8', u'\u76f8\u5c06', u'\u7ea4\u624b', u'\u4e1c\u897f',
         u'\u4e2d\u6709', u'\u4e91\u98de', u'\u65e0\u9645', u'\u6d88\u5f97',
         u'\u6eaa\u5c71', u'\u767e\u82b1', u'\u90a3\u66f4', u'\u957f\u662f',
         u'\u4e00\u5929', u'\u4e91\u96e8', u'\u4eba\u610f', u'\u91cd\u89c1',
         u'\u4eba\u5982', u'\u521d\u5ea6', u'\u5c18\u57c3', u'\u675c\u9e43',
         u'\u6781\u76ee', u'\u6eaa\u4e0a', u'\u7bab\u9f13', u'\u7ea2\u5986',
         u'\u81ea\u53e4', u'\u98ce\u6e05', u'\u4e0e\u8c01', u'\u4e91\u5c71',
         u'\u51b7\u843d', u'\u51c9\u751f', u'\u5f71\u91cc', u'\u65e0\u7aef',
         u'\u6625\u6c34', u'\u6b64\u53bb', u'\u7389\u58f6', u'\u82b1\u9634',
         u'\u96be\u5fd8', u'\u53c8\u4f55', u'\u58f0\u58f0', u'\u591a\u65f6',
         u'\u5982\u68a6', u'\u7f57\u8863', u'\u9752\u697c', u'\u9999\u98ce',
         u'\u5173\u5c71', u'\u5343\u91d1', u'\u592a\u5b88', u'\u671b\u65ad',
         u'\u671d\u6765', u'\u957f\u6c5f', u'\u4e0d\u8001', u'\u659c\u65e5',
         u'\u6709\u65f6', u'\u6e05\u591c', u'\u753b\u6865', u'\u79cb\u58f0',
         u'\u8001\u77e3', u'\u597d\u5728', u'\u5c4f\u5c71', u'\u6625\u4e0d',
         u'\u6625\u6101', u'\u6c88\u9189', u'\u6e56\u5c71', u'\u72b9\u81ea',
         u'\u7559\u6625', u'\u8f7d\u9152', u'\u9662\u843d', u'\u98ce\u666f',
         u'\u4e00\u68a6', u'\u54ab\u5c3a', u'\u591c\u5bd2', u'\u66f4\u65e0',
         u'\u6708\u4e0a', u'\u6b8b\u7ea2', u'\u6c34\u4e91', u'\u6ee1\u57ce',
         u'\u72ec\u7acb', u'\u7389\u697c', u'\u73b2\u73d1', u'\u8885\u8885',
         u'\u98ce\u91cc', u'\u5c81\u665a', u'\u6731\u6237', u'\u7eff\u9b13',
         u'\u9752\u6625', u'\u4e09\u5e74', u'\u4e94\u4e91', u'\u534e\u5802',
         u'\u5357\u697c', u'\u53bb\u4e5f', u'\u5929\u7136', u'\u65e5\u957f',
         u'\u72b9\u5728', u'\u82b1\u95f4', u'\u4e0d\u59a8', u'\u4e16\u4e8b',
         u'\u51e0\u591a', u'\u5fae\u96e8', u'\u6559\u4eba', u'\u65b0\u58f0',
         u'\u6708\u534e', u'\u6e38\u4eba', u'\u8001\u6765', u'\u8349\u8349',
         u'\u4ece\u5bb9', u'\u591c\u96e8', u'\u65b0\u8bcd', u'\u770b\u82b1',
         u'\u9189\u4e61', u'\u4fee\u7af9', u'\u5c71\u8272', u'\u7591\u662f',
         u'\u79bb\u522b', u'\u832b\u832b', u'\u83ba\u58f0', u'\u8457\u610f',
         u'\u8bb8\u591a', u'\u9999\u96fe', u'\u4e00\u6795', u'\u4e34\u6c34',
         u'\u4f11\u95ee', u'\u82b1\u65e0', u'\u9633\u6625', u'\u4eba\u4e16',
         u'\u541b\u738b', u'\u5bfb\u82b3', u'\u5c3d\u65e5', u'\u65b0\u6101',
         u'\u65b0\u6708', u'\u6b64\u60c5', u'\u826f\u8fb0', u'\u98ce\u7ec6',
         u'\u4e39\u9752', u'\u53e4\u4eca', u'\u5fc3\u60c5', u'\u6625\u68a6',
         u'\u8001\u4eba', u'\u96f6\u843d', u'\u6b63\u662f', u'\u6e0a\u660e',
         u'\u8377\u82b1', u'\u94f6\u70db', u'\u4f24\u6625', u'\u5929\u4e0b',
         u'\u6c34\u8fb9', u'\u8109\u8109', u'\u4e0d\u9053', u'\u53ef\u60dc',
         u'\u5929\u9645', u'\u5bb6\u5c71', u'\u5f52\u65f6', u'\u758f\u96e8',
         u'\u767d\u4e91', u'\u4e94\u6e56', u'\u4eba\u77e5', u'\u65e5\u66ae',
         u'\u65e7\u65e5', u'\u82b1\u5e95', u'\u90fd\u662f', u'\u9690\u9690',
         u'\u522b\u6709', u'\u6653\u6765', u'\u6b64\u9645', u'\u6e05\u6653',
         u'\u4eba\u9759', u'\u4f55\u66fe', u'\u5929\u98ce', u'\u6765\u65e0',
         u'\u89c1\u8bf4', u'\u4e09\u6708', u'\u4e0d\u80fd', u'\u4e3a\u6211',
         u'\u53bb\u540e', u'\u6d6e\u4e91', u'\u7eff\u6768', u'\u7f8e\u4eba',
         u'\u81ea\u662f', u'\u897f\u56ed', u'\u9e25\u9e6d', u'\u4e0d\u80dc',
         u'\u4eba\u60c5', u'\u672a\u8001', u'\u6e3a\u6e3a', u'\u94f6\u6cb3',
         u'\u5189\u5189', u'\u7389\u5802', u'\u592a\u5e73', u'\u6000\u62b1',
         u'\u6545\u56ed', u'\u65b0\u6765', u'\u6f20\u6f20', u'\u758f\u5f71',
         u'\u591c\u6708', u'\u65b0\u5986', u'\u6c34\u8c03', u'\u72b9\u6709',
         u'\u7b2c\u4e00', u'\u82b1\u65f6', u'\u987b\u4fe1', u'\u4e00\u6625',
         u'\u5f52\u671f', u'\u70b9\u70b9', u'\u95fb\u9053', u'\u56de\u5934',
         u'\u5929\u9999', u'\u6570\u58f0', u'\u65e0\u5fc3', u'\u70df\u6ce2',
         u'\u7559\u8fde', u'\u8fe2\u8fe2', u'\u4f73\u671f', u'\u6005\u671b',
         u'\u6ee1\u773c', u'\u72b9\u672a', u'\u8c01\u80fd', u'\u4e0d\u65ad',
         u'\u4e91\u6df1', u'\u7279\u5730', u'\u771f\u4e2a', u'\u8f7b\u5bd2',
         u'\u98de\u82b1', u'\u4eba\u4f55', u'\u4eba\u7269', u'\u4f9d\u7ea6',
         u'\u51e0\u56de', u'\u6c5f\u6885', u'\u72ec\u81ea', u'\u4f55\u5728',
         u'\u534e\u53d1', u'\u6f47\u6d12', u'\u4e07\u9877', u'\u5524\u8d77',
         u'\u65e0\u529b', u'\u770b\u53d6', u'\u8c08\u7b11', u'\u538c\u538c',
         u'\u56ed\u6797', u'\u65e5\u6708', u'\u6625\u4e8b', u'\u665a\u6765',
         u'\u753b\u697c', u'\u4eba\u4eba', u'\u5343\u8f7d', u'\u5411\u4eba',
         u'\u597d\u662f', u'\u6b64\u610f', u'\u6e05\u9999', u'\u72b9\u8bb0',
         u'\u98ce\u5473', u'\u4e00\u53f6', u'\u4eba\u5f52', u'\u53cc\u71d5',
         u'\u51dd\u4f2b', u'\u5e18\u680a', u'\u706f\u706b', u'\u897f\u697c',
         u'\u5357\u679d', u'\u522b\u6765', u'\u522b\u79bb', u'\u5c0f\u7a97',
         u'\u5e74\u6765', u'\u72ec\u501a', u'\u77e5\u5426', u'\u79cb\u6c34',
         u'\u8fdc\u5c71', u'\u4e3a\u541b', u'\u6f47\u6e58', u'\u9713\u88f3',
         u'\u98d8\u96f6', u'\u5c71\u4e2d', u'\u5e7f\u5bd2', u'\u60c5\u7eea',
         u'\u8bf4\u4e0e', u'\u4f55\u8bb8', u'\u5c0f\u697c', u'\u5f53\u65e5',
         u'\u7476\u53f0', u'\u79cb\u5149', u'\u82f1\u96c4', u'\u98de\u53bb',
         u'\u5357\u6d66', u'\u68a7\u6850', u'\u884c\u4e50', u'\u68a6\u56de',
         u'\u82b1\u4e0b', u'\u957f\u4ead', u'\u4e1c\u7bf1', u'\u4e8c\u5341',
         u'\u4eca\u5915', u'\u4f9d\u4f9d', u'\u5929\u5730', u'\u68a6\u65ad',
         u'\u6e05\u6b4c', u'\u76ee\u65ad', u'\u7b11\u8bed', u'\u4e50\u4e8b',
         u'\u6df1\u6df1', u'\u7261\u4e39', u'\u82b1\u843d', u'\u82b3\u5fc3',
         u'\u4e00\u5c0a', u'\u603b\u662f', u'\u6ee1\u5730', u'\u753b\u5802',
         u'\u95f2\u6101', u'\u4e09\u5341', u'\u51cc\u6ce2', u'\u5343\u4e07',
         u'\u87e0\u6843', u'\u9ad8\u697c', u'\u4f55\u65e5', u'\u51ed\u8c01',
         u'\u7eff\u9634', u'\u8fc7\u4e86', u'\u4e0d\u7981', u'\u5149\u9634',
         u'\u60c5\u6000', u'\u5982\u6c34', u'\u6c88\u6c88', u'\u79bb\u6101',
         u'\u7fe0\u8896', u'\u90a3\u582a', u'\u4ece\u6b64', u'\u51ed\u9611',
         u'\u8c01\u4e0e', u'\u5357\u5c71', u'\u68a6\u4e2d', u'\u843d\u65e5',
         u'\u9189\u91cc', u'\u65e7\u6e38', u'\u6625\u610f', u'\u68a6\u9b42',
         u'\u9633\u5173', u'\u98ce\u524d', u'\u5343\u5c81', u'\u5e94\u662f',
         u'\u6697\u9999', u'\u4e0d\u5c3d', u'\u5a75\u5a1f', u'\u6c5f\u5934',
         u'\u53c8\u8fd8', u'\u79cb\u8272', u'\u96e8\u8fc7', u'\u4e0e\u541b',
         u'\u5c81\u5c81', u'\u679d\u5934', u'\u80ed\u8102', u'\u4e09\u5343',
         u'\u53c2\u5dee', u'\u679d\u4e0a', u'\u85b0\u98ce', u'\u4e0d\u7528',
         u'\u77e5\u9053', u'\u8bd5\u95ee', u'\u65e0\u7a77', u'\u8001\u5b50',
         u'\u82b3\u83f2', u'\u4f55\u4f3c', u'\u4f55\u987b', u'\u4e16\u95f4',
         u'\u4f55\u5982', u'\u65e5\u65e5', u'\u6625\u53bb', u'\u674f\u82b1',
         u'\u6c5f\u6e56', u'\u77e5\u4f55', u'\u91cd\u91cd', u'\u65e0\u5904',
         u'\u6b4c\u58f0', u'\u7761\u8d77', u'\u8001\u53bb', u'\u5218\u90ce',
         u'\u6768\u82b1', u'\u7476\u6c60', u'\u4e3b\u4eba', u'\u5343\u5e74',
         u'\u6708\u4e0b', u'\u6c60\u5858', u'\u7ec6\u96e8', u'\u4e00\u9189',
         u'\u4e07\u4e8b', u'\u65e0\u8ba1', u'\u66ae\u4e91', u'\u6b64\u65f6',
         u'\u7435\u7436', u'\u4ece\u6765', u'\u4f7f\u541b', u'\u7389\u4eba',
         u'\u9752\u9752', u'\u626c\u5dde', u'\u6587\u7ae0', u'\u70df\u6c34',
         u'\u82b1\u5f71', u'\u7ea2\u5c18', u'\u7eb7\u7eb7', u'\u5357\u5317',
         u'\u628a\u9152', u'\u6625\u5149', u'\u8fd8\u662f', u'\u4e0d\u4f4f',
         u'\u4ed8\u4e0e', u'\u65e0\u8a00', u'\u6625\u5bd2', u'\u4eba\u5bb6',
         u'\u5e18\u5377', u'\u697c\u4e0a', u'\u6709\u8c01', u'\u68a6\u91cc',
         u'\u767e\u5e74', u'\u98de\u6765', u'\u4e0d\u6210', u'\u51e0\u756a',
         u'\u8d62\u5f97', u'\u4e00\u65f6', u'\u4e0d\u5230', u'\u5f52\u8def',
         u'\u5bb9\u6613', u'\u78a7\u4e91', u'\u5e74\u534e', u'\u98de\u7d6e',
         u'\u957f\u751f', u'\u5e95\u4e8b', u'\u60c6\u6005', u'\u4e0d\u7ba1',
         u'\u6df1\u9662', u'\u697c\u53f0', u'\u4eba\u4e0d', u'\u53ea\u6050',
         u'\u548c\u6c14', u'\u591c\u6df1', u'\u6765\u65f6', u'\u767b\u4e34',
         u'\u82b1\u679d', u'\u6625\u6765', u'\u95e8\u5916', u'\u4e00\u676f',
         u'\u767d\u53d1', u'\u7b49\u95f2', u'\u4e00\u5e74', u'\u4e7e\u5764',
         u'\u4eba\u53bb', u'\u8c01\u5bb6', u'\u5f98\u5f8a', u'\u6731\u989c',
         u'\u5e74\u5c11', u'\u51e0\u8bb8', u'\u73e0\u5e18', u'\u522b\u540e',
         u'\u65e0\u5948', u'\u8427\u8427', u'\u4e2d\u79cb', u'\u4eca\u53e4',
         u'\u501a\u9611', u'\u91cd\u6765', u'\u91cd\u9633', u'\u4eca\u671d',
         u'\u660e\u65e5', u'\u76f8\u89c1', u'\u9ec4\u91d1', u'\u4f55\u59a8',
         u'\u82b1\u98de', u'\u70df\u96e8', u'\u81ea\u6709', u'\u82b1\u524d',
         u'\u53ef\u601c', u'\u79cb\u5343', u'\u5148\u751f', u'\u6bb7\u52e4',
         u'\u884c\u4e91', u'\u4e00\u591c', u'\u591c\u6765', u'\u91d1\u7f15',
         u'\u4ece\u4eca', u'\u65e7\u65f6', u'\u4eca\u5bb5', u'\u5bd2\u98df',
         u'\u643a\u624b', u'\u6b4c\u821e', u'\u76c8\u76c8', u'\u5206\u660e',
         u'\u82b1\u5f00', u'\u98ce\u5149', u'\u53c8\u662f', u'\u7cbe\u795e',
         u'\u4e0d\u5982', u'\u4f9d\u7136', u'\u76f8\u5bf9', u'\u5ead\u9662',
         u'\u65e0\u8bed', u'\u9152\u9192', u'\u4e0d\u987b', u'\u53ea\u6709',
         u'\u8bb0\u5f97', u'\u4e0d\u582a', u'\u660e\u671d', u'\u6e05\u98ce',
         u'\u79cb\u98ce', u'\u7f25\u7f08', u'\u5e18\u5e55', u'\u98ce\u9732',
         u'\u5206\u4ed8', u'\u5915\u9633', u'\u6709\u4eba', u'\u51e0\u65f6',
         u'\u601d\u91cf', u'\u6625\u5f52', u'\u5782\u6768', u'\u5e74\u65f6',
         u'\u5341\u91cc', u'\u5982\u8bb8', u'\u4eca\u5e74', u'\u4f55\u4eba',
         u'\u68a8\u82b1', u'\u4e00\u756a', u'\u6628\u591c', u'\u6c5f\u5c71',
         u'\u5982\u6b64', u'\u7b19\u6b4c', u'\u4e1c\u541b', u'\u4eba\u5728',
         u'\u5343\u53e4', u'\u660e\u5e74', u'\u5929\u6c14', u'\u5341\u4e8c',
         u'\u65e0\u6570', u'\u71d5\u5b50', u'\u5982\u4f55', u'\u843d\u82b1',
         u'\u51e0\u5ea6', u'\u6e05\u660e', u'\u6708\u660e', u'\u5bcc\u8d35',
         u'\u60df\u6709', u'\u65f6\u5019', u'\u884c\u4eba', u'\u4e0d\u4f3c',
         u'\u4e00\u66f2', u'\u5f80\u4e8b', u'\u60a0\u60a0', u'\u8c01\u77e5',
         u'\u5bc2\u5bde', u'\u4eca\u591c', u'\u4f55\u65f6', u'\u65e0\u60c5',
         u'\u4e0d\u662f', u'\u9752\u5c71', u'\u4e3a\u8c01', u'\u80a0\u65ad',
         u'\u6c5f\u4e0a', u'\u84ec\u83b1', u'\u5c11\u5e74', u'\u65ad\u80a0',
         u'\u9e33\u9e2f', u'\u4f73\u4eba', u'\u53bb\u5e74', u'\u800c\u4eca',
         u'\u4e00\u58f0', u'\u5341\u5e74', u'\u6d77\u68e0', u'\u795e\u4ed9',
         u'\u6843\u674e', u'\u957f\u5b89', u'\u4e00\u7247', u'\u5341\u5206',
         u'\u5fc3\u4e8b', u'\u6d88\u606f', u'\u4eba\u751f', u'\u9ec4\u82b1',
         u'\u8299\u84c9', u'\u4f55\u4e8b', u'\u6194\u60b4', u'\u4eca\u65e5',
         u'\u4e00\u70b9', u'\u6843\u82b1', u'\u5929\u4e0a', u'\u6768\u67f3',
         u'\u6241\u821f', u'\u897f\u6e56', u'\u529f\u540d', u'\u65e0\u9650',
         u'\u5306\u5306', u'\u6625\u8272', u'\u65f6\u8282', u'\u5e73\u751f',
         u'\u51c4\u51c9', u'\u6df1\u5904', u'\u4e0d\u89c1', u'\u65e0\u4eba',
         u'\u659c\u9633', u'\u4e00\u679d', u'\u591a\u60c5', u'\u6545\u4eba',
         u'\u4e0d\u77e5', u'\u98ce\u6708', u'\u5f53\u65f6', u'\u4f9d\u65e7',
         u'\u98ce\u5439', u'\u6d41\u6c34', u'\u9ec4\u660f', u'\u5c0a\u524d',
         u'\u98ce\u96e8', u'\u5f53\u5e74', u'\u82b3\u8349', u'\u76f8\u9022',
         u'\u5929\u6daf', u'\u5e74\u5e74', u'\u4e00\u7b11', u'\u4e07\u91cc',
         u'\u9611\u5e72', u'\u591a\u5c11', u'\u5982\u4eca', u'\u56de\u9996',
         u'\u660e\u6708', u'\u5343\u91cc', u'\u6885\u82b1', u'\u6c5f\u5357',
         u'\u76f8\u601d', u'\u5f52\u6765', u'\u897f\u98ce', u'\u6625\u98ce',
         u'\u5f52\u53bb', u'\u98ce\u6d41', u'\u4eba\u95f4', u'\u4f55\u5904',
         u'\u4e1c\u98ce']


## ========================================


def satisfy_ping_ze(ping_ze, words):
    for a, b in zip(ping_ze, words):
        if a == u'中':
            continue
        elif a == b:
            continue
        else:
            return False
    return True


def is_good_engough(sent):
    if len(sent) != len(set(sent)):
        print 'bad'
        return False
    return True

def make_seg(yunlv):
    ping_ze = yunlv.group()
    num = len(yunlv.group())
    num_of_words = num / 2
    need_char = num % 2
    ret = ''
    while satisfy_ping_ze(ping_ze, ret) and is_good_engough(ret):
        segs = [random.choice(words) for _ in range(num_of_words)]
        if need_char:
            segs.append(random.choice(chars))
            # random swap
            if random.randint(0,2) == 0:
                segs[-2], segs[-1] = segs[-1], segs[-2]
        ret = u''.join(segs)

    return ret


def make_ci_from_ci_pai(ci_pai):

    str=u''.join(words)
    # print str

    cha=u''.join(chars)

    # print cha

    pattern = re.compile(u'([平仄中]+)', re.U)
    return re.sub(pattern, make_seg, ci_pai)


if __name__ == '__main__':
#    for i in words:
#        print i, utils.to_ping_ze(i)
    ci_pai = u"中仄中平平仄，中平中仄平平。中平中仄仄平平，中仄平平中仄。\n" \
             u"中仄中平平仄，中平中仄平平。中平中仄仄平平，中仄平平中仄。"
    ci_pai = u'中平中仄平平仄 中平中仄平平仄\n中仄中平平 中平平仄平\n中平平仄仄 中仄平平仄\n中仄仄平平 中平中仄平'
    title = u'凤凰台上忆吹箫'
    ci_pai1 = u"平仄平平，仄平平仄，仄平平仄平平。\n仄仄平平仄，仄仄平平。\n平仄平平仄仄，平仄仄、仄仄平平。\n" \
             u"平平仄，平平仄仄，仄仄平平。\n平平，仄平仄仄，平仄仄平平，仄仄平平。\n仄仄平平仄，平仄平平。\n" \
             u"平仄平平平仄，平仄仄、平仄平平。\n平平仄，平平仄平，仄仄平平。"
 #    title = u"忆江南"
 #    ci_pai = u"""平中仄
 # 中仄仄平平
 # 中仄中平平仄仄
 # 中平中仄仄平平
 # 中仄仄平平"""

    # title = u"测试词牌"
    # ci_pai = u"""仄仄仄"""



    print ('===', title, '===')
    print (make_ci_from_ci_pai(ci_pai))
