import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import VideoStreamers from "../video-streamers";
import  {global} from "../../config";
//import { fakeObjectOfInterest } from "./test-data/fakeObjectOfInterest";


 

let container = null;
beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it("renders VideoStreamers data", async () => {
    const fakeVideoStreamers = {
        cameras:[{cam:0,url:'http://203.77.210.41:2000/mjpg/video.mjpg'}, {cam:1,url:'http://203.77.210.41:2000/mjpg/video.mjpg'},{cam:2,url:'http://203.77.210.41:2000/mjpg/video.mjpg'}, {cam:3,url:'http://203.77.210.41:2000/mjpg/video.mjpg'}],
        objectOfInterests: ['car','person','cat', 'dog', 'track', 'motobike']
    }

 /* fix it
  jest.spyOn(VideoStreamers.prototype, "fetch").mockImplementation(() =>
  Promise.resolve({
    json: () => Promise.resolve(fakeVideoStreamers)
  })

);
  */

// Use the asynchronous version of act to apply resolved promises
await act(async () => {
  render(<VideoStreamers videoalignment={'both'}/>, container);
});


//expect(container.querySelector("img").getAttribute('class')).toBe('img_thumb');
//expect(container.querySelector("img").getAttribute('src')).toBe('data:image/jpeg;base64');
//expect(container.querySelector("img").getAttribute('id')).toBe('ABCF23422323');
//expect(container.querySelector("#ABCF23422324").getAttribute('id')).toBe('ABCF23422324');

// remove the mock to ensure tests are completely isolated
global.fetch.mockRestore();
});