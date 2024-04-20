### About This Project

This is a simple voice assistant. There are many like it, but this one is mine.

I am developing this project for a few reasons:

- I don't personally like the privacy/convenience ratio of Alexa and other home assistants
- I want skills that other voice assistants don't have, and I don't feel like developing skills for those devices. Perhaps someday I will do that as a possible income stream, if the skills seem useful enough for enough people, but for now I just want to build things exactly for my own needs
- To keep in Python practice. Right now I work exclusively in Javascript, with a heavy emphasis on frontend, and I want to keep my hand in other technologies and paradigms
- To keep in writing practice. Publish or perish, as they say, and it's been a long time since I've written much of anything
- I enjoy modular projects like this, where it is really easy to add incremental improvements over time
- To play with the raspberry pi
- Reduce screen time? In theory if I get all the planned skills up and running I'll be looking at my phone and navigating through different tabs less. The time saving there is probably nominal, though; this is mostly just a for-fun project
- Eventual language model integration experiments


#### Gotchas 
MacOS may need to install
`brew install portaudio`
`brew install flac`

to resolve errors with a mac M1 chip

On raspberry pi os need to run
`sudo apt install libespeak1`
`sudo apt install build-essential portaudio19-dev`
`sudo apt install flac`

For some reason, the line `import sounddevice` got rid of about a hundred ALSA library errors.

When setting up the .system script, need to specify default audio card or alsa will choke. Follow [instructions here](https://www.alsa-project.org/wiki/Setting_the_default_device) for simplest solution
