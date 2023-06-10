import json
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cv2
import shutil
import os
import subprocess
import argparse
import glob
from tqdm import tqdm
import time

"""
提取每个图片对应的category与bbox值，写入json然后转成需要的VOC格式
"""

# cellphone:79 key:266 handbag:13 laptop:77
# classes_names = {79: "cellphone", 266: "key", 13: "handbag", 77: "laptop"}
# classes_names = {79: "cell phone", 13: "handbag", 77: "laptop"}
classes_names_all =  {
1:"human",
2:"sneakers",
3:"chair",
4:"hat",
5:"lamp",
6:"bottle",
7:"cabinet/shelf",
8:"cup",
9:"car",
10:"glasses",
11:"picture/frame",
12:"desk",
13:"handbag",
14:"street lights",
15:"book",
16:"plate",
17:"helmet",
18:"leather shoes",
19:"pillow",
20:"glove",
21:"potted plant",
22:"bracelet",
23:"flower",
24:"monitor",
25:"storage box",
26:"plants pot/vase",
27:"bench",
28:"wine glass",
29:"boots",
30:"dining table",
31:"umbrella",
32:"boat",
33:"flag",
34:"speaker",
35:"trash bin/can",
36:"stool",
37:"backpack",
38:"sofa",
39:"belt",
40:"carpet",
41:"basket",
42:"towel/napkin",
43:"slippers",
44:"bowl",
45:"barrel/bucket",
46:"coffee table",
47:"suv",
48:"toy",
49:"tie",
50:"bed",
51:"traffic light",
52:"pen/pencil",
53:"microphone",
54:"sandals",
55:"canned",
56:"necklace",
57:"mirror",
58:"faucet",
59:"bicycle",
60:"bread",
61:"high heels",
62:"ring",
63:"van",
64:"watch",
65:"combine with bowl",
66:"sink",
67:"horse",
68:"fish",
69:"apple",
70:"traffic sign",
71:"camera",
72:"candle",
73:"stuffed animal",
74:"cake",
75:"motorbike/motorcycle",
76:"wild bird",
77:"laptop",
78:"knife",
79:"cell phone",
80:"paddle",
81:"truck",
82:"cow",
83:"power outlet",
84:"clock",
85:"drum",
86:"fork",
87:"bus",
88:"hanger",
89:"nightstand",
90:"pot/pan",
91:"sheep",
92:"guitar",
93:"traffic cone",
94:"tea pot",
95:"keyboard",
96:"tripod",
97:"hockey stick",
98:"fan",
99:"dog",
100:"spoon",
101:"blackboard/whiteboard",
102:"balloon",
103:"air conditioner",
104:"cymbal",
105:"mouse",
106:"telephone",
107:"pickup truck",
108:"orange",
109:"banana",
110:"airplane",
111:"luggage",
112:"skis",
113:"soccer",
114:"trolley",
115:"oven",
116:"remote",
117:"combine with glove",
118:"paper towel",
119:"refrigerator",
120:"train",
121:"tomato",
122:"machinery vehicle",
123:"tent",
124:"shampoo/shower gel",
125:"head phone",
126:"lantern",
127:"donut",
128:"cleaning products",
129:"sailboat",
130:"tangerine",
131:"pizza",
132:"kite",
133:"computer box",
134:"elephant",
135:"toiletries",
136:"gas stove",
137:"broccoli",
138:"toilet",
139:"stroller",
140:"shovel",
141:"baseball bat",
142:"microwave",
143:"skateboard",
144:"surfboard",
145:"surveillance camera",
146:"gun",
147:"Life saver",
148:"cat",
149:"lemon",
150:"liquid soap",
151:"zebra",
152:"duck",
153:"sports car",
154:"giraffe",
155:"pumpkin",
156:"Accordion/keyboard/piano",
157:"radiator",
158:"converter",
159:"tissue",
160:"carrot",
161:"washing machine",
162:"vent",
163:"cookies",
164:"cutting/chopping board",
165:"tennis racket",
166:"candy",
167:"skating and skiing shoes",
168:"scissors",
169:"folder",
170:"baseball",
171:"strawberry",
172:"bow tie",
173:"pigeon",
174:"pepper",
175:"coffee machine",
176:"bathtub",
177:"snowboard",
178:"suitcase",
179:"grapes",
180:"ladder",
181:"pear",
182:"american football",
183:"basketball",
184:"potato",
185:"paint brush",
186:"printer",
187:"billiards",
188:"fire hydrant",
189:"goose",
190:"projector",
191:"sausage",
192:"fire extinguisher",
193:"extension cord",
194:"facial mask",
195:"tennis ball",
196:"chopsticks",
197:"Electronic stove and gas stove",
198:"pie",
199:"frisbee",
200:"kettle",
201:"hamburger",
202:"golf club",
203:"cucumber",
204:"clutch",
205:"blender",
206:"tong",
207:"slide",
208:"hot dog",
209:"toothbrush",
210:"facial cleanser",
211:"mango",
212:"deer",
213:"egg",
214:"violin",
215:"marker",
216:"ship",
217:"chicken",
218:"onion",
219:"ice cream",
220:"tape",
221:"wheelchair",
222:"plum",
223:"bar soap",
224:"scale",
225:"watermelon",
226:"cabbage",
227:"router/modem",
228:"golf ball",
229:"pine apple",
230:"crane",
231:"fire truck",
232:"peach",
233:"cello",
234:"notepaper",
235:"tricycle",
236:"toaster",
237:"helicopter",
238:"green beans",
239:"brush",
240:"carriage",
241:"cigar",
242:"earphone",
243:"penguin",
244:"hurdle",
245:"swing",
246:"radio",
247:"CD",
248:"parking meter",
249:"swan",
250:"garlic",
251:"french fries",
252:"horn",
253:"avocado",
254:"saxophone",
255:"trumpet",
256:"sandwich",
257:"cue",
258:"kiwi fruit",
259:"bear",
260:"fishing rod",
261:"cherry",
262:"tablet",
263:"green vegetables",
264:"nuts",
265:"corn",
266:"key",
267:"screwdriver",
268:"globe",
269:"broom",
270:"pliers",
271:"hammer",
272:"volleyball",
273:"eggplant",
274:"trophy",
275:"board eraser",
276:"dates",
277:"rice",
278:"tape measure/ruler",
279:"dumbbell",
280:"hamimelon",
281:"stapler",
282:"camel",
283:"lettuce",
284:"goldfish",
285:"meat balls",
286:"medal",
287:"toothpaste",
288:"antelope",
289:"shrimp",
290:"rickshaw",
291:"trombone",
292:"pomegranate",
293:"coconut",
294:"jellyfish",
295:"mushroom",
296:"calculator",
297:"treadmill",
298:"butterfly",
299:"egg tart",
300:"cheese",
301:"pomelo",
302:"pig",
303:"race car",
304:"rice cooker",
305:"tuba",
306:"crosswalk sign",
307:"papaya",
308:"hair dryer",
309:"green onion",
310:"chips",
311:"dolphin",
312:"sushi",
313:"urinal",
314:"donkey",
315:"electric drill",
316:"spring rolls",
317:"tortoise/turtle",
318:"parrot",
319:"flute",
320:"measuring cup",
321:"shark",
322:"steak",
323:"poker card",
324:"binoculars",
325:"llama",
326:"radish",
327:"noodles",
328:"mop",
329:"yak",
330:"crab",
331:"microscope",
332:"barbell",
333:"Bread/bun",
334:"baozi",
335:"lion",
336:"red cabbage",
337:"polar bear",
338:"lighter",
339:"mangosteen",
340:"seal",
341:"comb",
342:"eraser",
343:"pitaya",
344:"scallop",
345:"pencil case",
346:"saw",
347:"table tennis  paddle",
348:"okra",
349:"starfish",
350:"monkey",
351:"eagle",
352:"durian",
353:"rabbit",
354:"game board",
355:"french horn",
356:"ambulance",
357:"asparagus",
358:"hoverboard",
359:"pasta",
360:"target",
361:"hotair balloon",
362:"chainsaw",
363:"lobster",
364:"iron",
365:"flashlight",
}
def save_annotations(classes_names, anno_file_path, imgs_file_path, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset):
    # open json file(val.json or train.json)
    print(classes_names)
    print("json load:", anno_file_path)
    with open(anno_file_path, 'r') as f:
        data = json.load(f)
        # 900w+
        print("anno count:", len(data["annotations"]))
        print("image count:", len(data["images"]))

        # 使用字典，只进行一遍json文件遍历节省时间
        img_map = {}
        img_2_anno = {}
        for i in data["images"]:
            img_map[i["id"]] = i
            img_2_anno[i["id"]] = []

        for anno in data["annotations"]:
            if anno["category_id"] in classes_names.keys():
                img_2_anno[anno["image_id"]].append(anno)

        for _, id in enumerate(img_2_anno):
            annos = img_2_anno[id]
            if len(annos) > 0:
                img = img_map[id]
                img_name = img["file_name"]
                img_width = img["width"]
                img_height = img["height"]

                objs = []
                for anno in annos:
                    bbox = anno["bbox"]
                    xmin = max(int(bbox[0]), 0)
                    ymin = max(int(bbox[1]), 0)
                    xmax = min(int(bbox[2] + bbox[0]), img_width)
                    ymax = min(int(bbox[3] + bbox[1]), img_height)
                    class_name = classes_names[anno["category_id"]]
                    obj = [class_name, xmin, ymin, xmax, ymax]
                    objs.append(obj)

                save_head(objs, imgs_file_path, img_name, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset, img_width, img_height)

    print(" 提取完成 ")


def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def write_txt(output_dir, anno_path, img_path, dataset):
    list_name = output_dir + '/annotations_xml_object_{}.txt'.format(dataset)
    if not os.path.exists(list_name):
        with open(list_name, 'w', encoding="utf=8") as fs:
            print(fs)
    with open(list_name, 'r', encoding='utf-8') as list_fs:
        with open(list_name, 'a+', encoding='utf-8') as list_f:
            lines = os.path.basename(anno_path) + "\t" + img_path + "\n"
            list_f.write(lines)


def write_xml(anno_path, objs, img_path, output_dir, head, objectstr, tailstr, dataset):
    with open(anno_path, 'w') as f:
        f.write(head)
        for obj in objs:
            f.write(objectstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
        f.write(tailstr)
        write_txt(output_dir, anno_path, img_path, dataset)


def save_head(objs, imgs_file_path, img_name, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset, img_width, img_height):
    # imgs = cv2.imread(os.path.join(imgs_file_path, img_name))
    anno_path = os.path.join(output_anno_dir, img_name[-26:-3] + "xml")

    # if (imgs.shape[2] == 1):
    #     print(img_name + " not a RGB image")
    #     return
    head = headstr % (img_name, img_width, img_height, 3)
    write_xml(anno_path, objs, img_name, output_dir, head, objectstr, tailstr, dataset)


def find_anno_img(input_dir):
    # According input dir path find Annotations dir and Images dir
    anno_dir = os.path.join(input_dir, "Annotations")
    img_dir = os.path.join(input_dir, "Images")
    return anno_dir, img_dir


def main_object365(input_dir, output_dir, headstr, tailstr, objectstr):
    # use ids match classes
    classes_names = classes_names_all

    anno_dir, img_dir = find_anno_img(input_dir)
    for dataset in ["train"]:
        # xml output dir path
        output_anno_dir = os.path.join(output_dir, dataset)
        if not os.path.exists(output_anno_dir):
            mkr(output_anno_dir)

        # read jsons file
        anno_file_path = os.path.join(anno_dir, dataset, dataset+".json")
        # read imgs file
        imgs_file_path = os.path.join(img_dir, dataset)
        save_annotations(classes_names, anno_file_path, imgs_file_path, output_anno_dir, output_dir,headstr, tailstr, objectstr, dataset)
