import React, { useState } from 'react';
import Head from 'next/head';

import styled from 'styled-components';
import Counter from '../components/Counter';
import TTS from '../components/Tts';
import MusicPlayer from '../components/musicPlayer';
import MusicSlider from '../components/Music/MusicSlider';

export default function Home() {
  const [text, setText] = useState<string>('자바스크립트');

  setTimeout(() => {
    // setText("타입스크립트")
  }, 1000);

  return (
    <div className="container">
      {/* <TTS /> */}

      <MusicSlider />
      <MusicPlayer />
    </div>
  );
}
