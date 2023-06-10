# Object 365 

This repo download [`Object365`](https://www.objects365.org/download.html) based upon [Ultralytics](https://github.com/ultralytics) [script](https://github.com/ultralytics/yolov5/blob/master/data/Objects365.yaml#L402)

```
python download.py
```

You can also convert Object365 annotation file to VOC format.(json to xml)
# Dependencies

```
pip install pycocotools
pip install six
pip install numpy
pip install tqdm
pip install opencv-python
```

# Run
```
python main.py --dataset object365 --input "*Path*" --output "*Path*"
```

# save filenames to txt
```
python save_filename.py
```

# move images to one folder
```
sh mv_file.sh
```
