from PIL import Image as PILImage
from .. import asyncronous
from .. import image
import cv2
import numpy as np
from enum import Enum
import time

class VideoFormat():
    "I would recommend using 'VideoFormatEnum', rather than instanciating me directly"
    def __init__(self, fileExtensionName, codecName) -> None:
        self.fileExtensionName: str = fileExtensionName # eg "mp4"
        self.codecName: str         = codecName         # eg"MP48"

    def __str__(self) -> str:
        return self.fileExtensionName

class VideoFormatEnum(Enum):
    "A comprehensive list of all video codecs you can choose from."
    MP4 = VideoFormat("mp4", "MP48")
    AVI = VideoFormat("avi", "XVID")
    GIF = VideoFormat("gif", "GIF4")
def getVideoFormatByFileExtensionAsStr(value: str) -> VideoFormat:
    for property in VideoFormatEnum:
        try:
            if property.value.fileExtensionName.lower() == value.lower():
                return property.value
        except Exception as exc:
            print(f'Exception in fast/video/video.py getVideoFormatByFileExtensionAsStr {exc}')

import os
import pathlib

import mss
import typing

def videoToImageList(video: typing.Union[cv2.VideoCapture, str], outputImageType: image.ImageTypeEnum, percentageOfFramesToKeep0to1:float = 1) -> list:
    "video is either a VideoCapture cv2 obj or an absolute file path"
    returnVal: list = []
    if isinstance(video, str):
        video = cv2.VideoCapture(video)

    stillReading, image_ = video.read()
    frame_count = 0
    framePercentage = 0
    while stillReading:
        framePercentage += percentageOfFramesToKeep0to1
        if framePercentage >= 1:
            framePercentage = framePercentage % percentageOfFramesToKeep0to1
            if outputImageType == image.ImageTypeEnum.CV2:
                appendVal = image_
            elif outputImageType == image.ImageTypeEnum.PILLOW:
                appendVal = image.openCVimageToPillowImage(image_)
            else:
                raise Exception("Unsupported/Invalid ImageTypeEnum value")
            returnVal.append(appendVal)
        stillReading, image_ = video.read()
        frame_count += 1
    return returnVal
    




class VideoRecorder():
    """Writes to disk during the actual recording, this means that even interrupted video recordings will still be saved - I believe with little risk of corruption.
    
    @todo add audio support, add camera support"""
    def __exit__(self):
        self.stopRecording()
    def __init__(self, filepathIncludingFilename: str, codec: VideoFormat = VideoFormatEnum.MP4.value, leftTopRightBottomRecordBoundingBox: list[int] = [1920,1080], framerate = 60, spawnRecordingFeedbackWindow = False, abortIfFileExists = True, replaySpeedMultiplier = 1, gifPercentageOfFramesToKeep0to1: float = 1) -> None:
        # print(f"## LOOK HERE\n\n\n{type(codec)} - {codec.fileExtensionName}")
        self.gifPercentageOfFramesToKeep0to1 = gifPercentageOfFramesToKeep0to1
        self.convertToGif = False
        if codec == VideoFormatEnum.GIF.value: # @note gif
            codec = VideoFormatEnum.MP4.value
            self.convertToGif = True
        self.replaySpeedMultiplier = replaySpeedMultiplier
        leftTopRightBottomRecordBoundingBox = [int(i) for i in leftTopRightBottomRecordBoundingBox]
        self.filepathIncludingFilename = filepathIncludingFilename.replace('\\', '/')
        if self.filepathIncludingFilename.__contains__('.'):
            self.filepathIncludingFilename = self.filepathIncludingFilename[:self.filepathIncludingFilename.rfind('.')]
        self.filepathIncludingFilenameAndExtension = self.filepathIncludingFilename + "." + codec.fileExtensionName
        self.abortIfFileExists = abortIfFileExists
        self.numberOfFrames = 0
        # filepathIncludingFilename = r"C:\Users\olliv\Desktop\pythonVideoRecordingTest\Recording.mp4"
        # filepathIncludingFilename = r"C:\Users\olliv\Desktop\pythonVideoRecordingTest\Recording.avi"
        self.codec = codec
        self.leftTopRightBottomRecordBoundingBox = leftTopRightBottomRecordBoundingBox
        self.resolutionInPixels = [leftTopRightBottomRecordBoundingBox[2] -leftTopRightBottomRecordBoundingBox[0], leftTopRightBottomRecordBoundingBox[3] -leftTopRightBottomRecordBoundingBox[1]]
        self.framerate = framerate
        self.spawnRecordingFeedbackWindow = spawnRecordingFeedbackWindow
        self.isRecording = False
        if pathlib.Path(self.filepathIncludingFilenameAndExtension).exists() and abortIfFileExists:
            self.abort = True
            print("VideoRecorder object: Path already exists, aborting")
            return
        else:
            self.abort = False
        self.mssInstance = mss.mss()

    def stopRecording(self):
        if self.abort:
            return
        else:
            self.abort = True
        self.isRecording = False
        # Release the Video writer
        self.videoWriterObject.release()
        
        # Destroy all windows
        if self.spawnRecordingFeedbackWindow:
            cv2.destroyAllWindows()


        if self.convertToGif: # @note gif
            PILImages: list[PILImage.Image] = videoToImageList(self.filepathIncludingFilenameAndExtension, image.ImageTypeEnum.PILLOW, self.gifPercentageOfFramesToKeep0to1)
            # @note the duration parameter is the time for each frame to display in milliseconds
            frameDurationInMs = 1000/self.framerate/self.gifPercentageOfFramesToKeep0to1
            frameDurationsInMs = [frameDurationInMs for img in PILImages]
            # PILImage.new()
            # PILImages[0].save(self.filepathIncludingFilename+".gif", save_all=True, append_images=PILImages[1:], optimize=False, duration=(time.time()-self.startRecordingTime)/self.numberOfFrames,loop=0)
            # PILImages[0].save(self.filepathIncludingFilename+".gif", save_all=True, append_images=PILImages[1:], optimize=False, duration=1/self.framerate*10,loop=0)
            for img in PILImages:
                img.duration =frameDurationInMs
                # @note Setting optimize=True only saves like 1/15 of the total filesize.
            PILImages[0].save(self.filepathIncludingFilename+".gif", save_all=True, append_images=PILImages[1:], optimize=False, duration=frameDurationInMs,loop=0)

    def _asyncPushFrameLoop(self):
        while self.isRecording:
            time.sleep(1/960*8) # Were sleeping a lot shorter than we would expect to need to to accomodate  for potential lag/latency. Turns out this isnt always enough still however.
            if self.lastFramePushTime + 1/self.framerate < time.time():
                self.pushFrame()

    def startRecording(self, pushFramesManually = False):
        if self.abort:
            return
        self.isRecording = True
        self.startRecordingTime = time.time()
        self.lastFramePushTime = time.time()
        
        # Creating a VideoWriter object
        self.videoWriterObject = cv2.VideoWriter(self.filepathIncludingFilenameAndExtension, cv2.VideoWriter_fourcc(*self.codec.codecName), self.framerate/self.replaySpeedMultiplier, (self.resolutionInPixels[0], self.resolutionInPixels[1]))
        
        if self.spawnRecordingFeedbackWindow:
            # Create an Empty window
            cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
            
            # Resize this window
            cv2.resizeWindow("Live", 480, 270)
        
        if not pushFramesManually:
            asyncronous.runAsync(self._asyncPushFrameLoop)
        
        

    def pushFrame(self):
        # print("push")
        if self.abort:
            return
        self.numberOfFrames += 1
        self.lastFramePushTime = time.time()
        # return
        # Take screenshot using PyAutoGUI
        img = self.mssInstance.grab({'left': self.leftTopRightBottomRecordBoundingBox[0], 'top': self.leftTopRightBottomRecordBoundingBox[1], 'width': self.leftTopRightBottomRecordBoundingBox[2]-self.leftTopRightBottomRecordBoundingBox[0], 'height': self.leftTopRightBottomRecordBoundingBox[3]-self.leftTopRightBottomRecordBoundingBox[1]})
        # img = pyautogui.screenshot()
    
        # print("push1")
        # Convert the screenshot to a numpy array
        frame = np.array(img)
    
        # print("push1.5")
        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # print("push2")
        # Write it to the output file
        self.videoWriterObject.write(frame)

        # print("push2.5")
        if self.spawnRecordingFeedbackWindow:
            # Optional: Display the recording screen
            pass
            # cv2.imshow('Live', frame) # @note causes a freeze?
        

        # Stop recording when we press 'q'
        # if cv2.waitKey(1) == ord('q'):
        #     break
        # print("push3")



# @note Example usecases
# videoRecorder = VideoRecorder(r"C:\Users\olliv\Desktop\pythonVideoRecordingTest\record", VideoFormatEnum.MP4.value, [0,0, 1920,1080], 30, True)
# videoRecorder.startRecording()
# time.sleep(5)
# videoRecorder.stopRecording()
# videoRecorder.numberOfFrames/30