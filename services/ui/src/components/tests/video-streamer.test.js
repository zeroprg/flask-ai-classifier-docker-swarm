import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import VideoStreamer from "./video-streamer";
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

it("renders VideoStreamer data", async () => {
  const fakeObjectOfInterest = [    { hashcode: 'ABCF23422323' , currenttime: 1601476686.8732808, frame: 'data:image/jpeg;base64'},
                                    { hashcode: 'ABCF23422324' , currenttime: 1601476686, frame: 'data:image/jpeg;base64'}   
  ]
  jest.spyOn(global, "fetch").mockImplementation(() =>
  Promise.resolve({
    json: () => Promise.resolve(fakeObjectOfInterest)
  })
);

// Use the asynchronous version of act to apply resolved promises
await act(async () => {
  render(<VideoStreamer camera={{url:'http://203.77.210.41:2000/mjpg/video.mjpg',cam:0}} object_of_interest={['car', 'person']} />, container);
});

expect(container.querySelector("#ABCF23422323").getAttribute('id')).toBe('ABCF23422323');
expect(container.querySelector("#ABCF23422324").getAttribute('id')).toBe('ABCF23422324');

// remove the mock to ensure tests are completely isolated
global.fetch.mockRestore();
});