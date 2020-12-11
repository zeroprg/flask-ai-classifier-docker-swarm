import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import Video from "./video";
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

it("renders Video data", async () => {

// Use the asynchronous version of act to apply resolved promises
await act(async () => {
  render(<Video camera={ {url:'http://203.77.210.41:2000/mjpg/video.mjpg', cam:0} } object_of_interest={['car', 'person']} />, container);
});

//expect(container.querySelector("b").getValue().toBe('http://203.77.210.41:2000/mjpg/video.mjpg');


});