from ultralytics import YOLO

model = YOLO('yolov5s.pt')

def main():
    model.train(data='Dataset/SplitData/data.yaml', epochs=3)


if __name__ == '__main__':
    main()
