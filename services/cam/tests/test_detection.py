import unittest
import cv2
from unittest.mock import patch
from project import Detection

class TestDetection(unittest.TestCase):
    
    def test_detection(self):
        # Video
        video = {
            'url': 'http://example.com/video_feed',
            'id': 1
        }
        # Classify server
        classify_server = 'http://example.com/classify'
        # Confidence
        confidence = 0.5
        # Model
        model = 'model'
        # OS
        os = 'test'
        # Create a detection object
        detection = Detection(os, classify_server, confidence, model, video)
        # Make sure the detection object has been created
        self.assertIsNotNone(detection)
        # Make sure the confidence level has been set correctly
        self.assertEqual(detection.confidence, confidence)
        # Make sure the model has been set correctly
        self.assertEqual(detection.model, model)
        # Make sure the video URL has been set correctly
        self.assertEqual(detection.video_url, video['url'])
        # Make sure the hashes are initialized
        self.assertEqual(len(detection.hashes), 0)
        # Make sure the topic label is initialized to 'no data'
        self.assertEqual(detection.topic_label, 'no data')
        # Make sure the net and video stream are initialized to None
        self.assertIsNone(detection.net)
        self.assertIsNone(detection.video_s)
        # Make sure the camera ID is set correctly
        self.assertEqual(detection.cam, str(video['id']))
        # Make sure the classify server has been set correctly
        self.assertEqual(detection.classify_server, classify_server)
        # Make sure the errors counter is initialized to 0
        self.assertEqual(detection.errors, 0)
        # Make sure the created time is set correctly
        self.assertAlmostEqual(detection.created_time, time.time()*1000, delta=1000)
        # Make sure the last update time is set correctly
        self.assertAlmostEqual(detection.last_update_time, time.time()*1000, delta=1000)
        # Make sure the idle time is initialized to 0
        self.assertEqual(detection.idle_time, 0)
        # Make sure the list of processes is initialized to an empty list
        self.assertEqual(len(detection.processes), 0)
        # Make sure the OS is set correctly
        self.assertEqual(detection.os, os)
        # Make sure the objects counted is initialized to 0
        self.assertEqual(detection._objects_counted.value, 0)
        
    @patch('project.detection.call_classifier_locally')
    def test_classify(self, mock_call_classifier_locally):
        # Video
        video = {
            'url': 'http://example.com/video_feed',
            'id': 1
        }
        # Classify server
        classify_server = 'http://example.com/classify'
        # Confidence
        confidence = 0.5
        # Model
        model = 'model'
        # OS
        os = 'test'
        # Create a detection object
        detection = Detection(os, classify_server, confidence, model, video)
        # Frame
        frame = cv2.imread('test_image.png')
        # Call classify method
        detection.classify()
        # Check if the call to the classifier was made
        self.assertTrue(mock_call_classifier_locally.called)
        
if __name__ == '__main__':
    unittest.main()
