import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import ObjectOfInterest from "../objects_of_interest";
import {global} from "../../config";
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

it("renders ObjectOfInterest data", async () => {
  const fakeObjectOfInterest = [ { hashcode: 'ABCF23422323' , currenttime: 1601476686.8732808, frame: 'data:image/jpeg;base64'},
                                 { hashcode: 'ABCF23422324' , currenttime: 1601476686, frame: 'data:image/jpeg;base64'}]
  jest.spyOn(global, "fetch").mockImplementation(() =>
  Promise.resolve({
    json: () => Promise.resolve(fakeObjectOfInterest)
  })
);

// Use the asynchronous version of act to apply resolved promises
await act(async () => {
  render(<ObjectOfInterest start={0} end={50} cam={0} object_of_interest={'car'} />, container);
});


expect(container.querySelector("img").getAttribute('class')).toBe('img_thumb');
expect(container.querySelector("img").getAttribute('src')).toBe('data:image/jpeg;base64');
expect(container.querySelector("img").getAttribute('id')).toBe('ABCF23422323');
expect(container.querySelector("#ABCF23422324").getAttribute('id')).toBe('ABCF23422324');

// remove the mock to ensure tests are completely isolated
global.fetch.mockRestore();
});