import React, { useState, useEffect, useRef } from 'react';

// Agent definitions
const agents = [
  { id: 'bytebeat', name: 'ByteBeat', emoji: '🎤', color: 'bg-purple-500', role: 'Songwriter', style: 'Bollywood Ballads' },
  { id: 'remixraja', name: 'RemixRaja', emoji: '🎧', color: 'bg-blue-500', role: 'Producer', style: 'Electronic Fusion' },
  { id: 'sursangam', name: 'SurSangam', emoji: '🎶', color: 'bg-pink-500', role: 'Classical', style: 'Ghazal & Sufi' },
  { id: 'rockstar', name: 'RockStar', emoji: '🎸', color: 'bg-red-500', role: 'Rock', style: 'Hindi Rock' },
];

const judge = { id: 'judge', name: 'The Judge', emoji: '⭐', color: 'bg-yellow-500' };
const hypeboi = { id: 'hypeboi', name: 'HypeBoi3000', emoji: '🔥', color: 'bg-orange-500' };

// Song database for autonomous play
const songDatabase = {
  'A': [
    { title: 'Aashiqui Mein Teri', lyrics: 'Aashiqui mein teri kho gaya main\nDil ki raahon mein so gaya main\nTere bina ab jeena mushkil\nHar pal tera hi naam liya main', end: 'N' },
    { title: 'Ankhen Teri', lyrics: 'Ankhen teri kitni haseen\nDekhun main tujhe har pal\nSapno mein bhi tu hai meri\nJaane kya hai ye kamal', end: 'L' },
  ],
  'B': [
    { title: 'Barish Ka Mausam', lyrics: 'Barish ka mausam aaya hai\nDil mera ghabraya hai\nTeri yaad mein bheega main\nAansuo ne rulaya hai', end: 'I' },
  ],
  'D': [
    { title: 'Dil Ki Baat', lyrics: 'Dil ki baat sunao zara\nPyaar ki raahon mein chalo sara\nSapne bune hain humne saath\nChhod na dena mera haath', end: 'T' },
    { title: 'Duniya Se Door', lyrics: 'Duniya se door jaake\nTere saath rehna hai\nHar pal tera hi sochke\nBas tujhse milna hai', end: 'I' },
  ],
  'E': [
    { title: 'Ek Pal Ki Khushi', lyrics: 'Ek pal ki khushi de de mujhe\nZindagi mein rang bhar de\nTera saath ho toh kaafi hai\nDuniya ki fikar chhod de', end: 'E' },
  ],
  'I': [
    { title: 'Ishq Tera', lyrics: 'Ishq tera mujhpe chhaya\nDil ne tujhe apnaya\nHar lamha tera hai ab\nTune mujhe pagal banaya', end: 'A' },
  ],
  'K': [
    { title: 'Khwabon Mein', lyrics: 'Khwabon mein aate ho tum\nDil ko churate ho tum\nJaago toh bhi sapna ho\nSote mein bhi yaad ho tum', end: 'M' },
  ],
  'L': [
    { title: 'Lamhon Ki Yeh', lyrics: 'Lamhon ki yeh kahaani\nLikh raha hoon main\nTere naam se shuru\nTere naam pe khatam', end: 'M' },
  ],
  'M': [
    { title: 'Mohabbat Ki Raahein', lyrics: 'Mohabbat ki raahein mushkil hain\nMagar tere saath chalenge\nHar mod pe tera haath thaam\nSaath jeeyenge marenge', end: 'E' },
    { title: 'Manzilein Apni', lyrics: 'Manzilein apni door hain\nRaaste bhi anjaane\nPar tera saath ho toh\nHar mushkil hai aasaan', end: 'N' },
  ],
  'N': [
    { title: 'Naina Milaake', lyrics: 'Naina milaake chale gaye\nDil mein yaadein de gaye\nWoh lamhe ab bhi zinda hain\nAankhon mein sapne base', end: 'E' },
    { title: 'Nazrein Mili', lyrics: 'Nazrein mili toh dil dhadka\nSaans ruki ek pal ko\nTere bina ab chain nahi\nKya karun is dil ko', end: 'O' },
  ],
  'O': [
    { title: 'O Saathi Re', lyrics: 'O saathi re tere bina\nJeena kaisa jeena\nTu hi meri manzil hai\nTujhpe hai mera yakeen', end: 'N' },
  ],
  'P': [
    { title: 'Pyaar Ki Yeh', lyrics: 'Pyaar ki yeh kahani\nLikhi maine tere naam\nHar pal mein teri yaad\nSubah se lekar shaam', end: 'M' },
  ],
  'R': [
    { title: 'Raaton Ki Tanhai', lyrics: 'Raaton ki tanhai mein\nTeri yaad aati hai\nChand bhi sharma ke\nBaadlon mein chhup jaata hai', end: 'I' },
  ],
  'S': [
    { title: 'Sapnon Ka Sheher', lyrics: 'Sapnon ka sheher basaya maine\nTere naam ka taara sajaya\nHar gali mein teri khushbu\nDil ne tujhe apnaya', end: 'A' },
  ],
  'T': [
    { title: 'Teri Yaadein', lyrics: 'Teri yaadein aati hain\nDil ko chu jaati hain\nBeet gaye jo pal saath\nWoh laut ke nahi aati hain', end: 'N' },
    { title: 'Tu Hi Mera', lyrics: 'Tu hi mera sab kuch hai\nTu hi meri duniya\nTere bina main kuch nahi\nBas tera hi hoon sajna', end: 'A' },
  ],
};

// Judge comments
const judgeComments = [
  "Wah wah! Kya baat hai! Smooth transition. 8/10",
  "Classic Bollywood vibes! The emotion is palpable. 7/10",
  "Now THAT'S how you play Antakshari! 9/10",
  "Clever letter transition! I see what you did there. 8/10",
  "The melody flows beautifully. Well played! 7/10",
  "Vintage romance with modern touch. Love it! 8/10",
  "A bit predictable, but executed well. 6/10",
  "Chef's kiss! This is Antakshari at its finest! 9/10",
];

// Hype comments
const hypeComments = [
  "BROOOOO THIS IS FIRE 🔥🔥🔥 I'M LITERALLY CRYING RN 😭💯",
  "KYA BAAT HAI YAAR!!! GOOSEBUMPS!! 🙌🙌🙌 #Legendary",
  "I WASN'T READY FOR THIS 😭🔥 CERTIFIED BANGER!!",
  "THIS SLAPS DIFFERENT AT 2AM BRO 💯🎵 #AntakshariKing",
  "PLAY THIS AT MY WEDDING!! 🎉🔥 ABSOLUTELY INSANE!!",
  "BRO DROPPED THIS AND LEFT US SPEECHLESS 😭💯🙌",
  "THE VIBES ARE IMMACULATE 🔥✨ #MasterClass",
  "I'VE LISTENED TO THIS 47 TIMES ALREADY 💯🎵🔥",
];

function getRandomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getSongForLetter(letter) {
  const songs = songDatabase[letter.toUpperCase()];
  if (songs && songs.length > 0) {
    return getRandomItem(songs);
  }
  // Fallback - find any song
  const allLetters = Object.keys(songDatabase);
  const fallbackLetter = getRandomItem(allLetters);
  return { ...getRandomItem(songDatabase[fallbackLetter]), forcedStart: fallbackLetter };
}

export default function AntakshariSpectator() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentLetter, setCurrentLetter] = useState('D');
  const [round, setRound] = useState(0);
  const [songs, setSongs] = useState([]);
  const [currentAgentIndex, setCurrentAgentIndex] = useState(0);
  const [phase, setPhase] = useState('idle'); // idle, thinking, singing, commenting
  const [thinkingText, setThinkingText] = useState('');
  const [currentSong, setCurrentSong] = useState(null);
  const [displayedLyrics, setDisplayedLyrics] = useState('');
  const [comments, setComments] = useState([]);
  const [speed, setSpeed] = useState(1);
  const feedRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [songs, comments, displayedLyrics]);

  // Main game loop
  useEffect(() => {
    if (!isPlaying) return;

    let timeout;
    const baseDelay = 1000 / speed;

    if (phase === 'thinking') {
      const thinkingMessages = [
        `Hmm... a song starting with "${currentLetter}"...`,
        `Let me think... "${currentLetter}"...`,
        `I got one! Starting with "${currentLetter}"...`,
      ];
      let msgIndex = 0;
      
      const thinkInterval = setInterval(() => {
        setThinkingText(thinkingMessages[msgIndex % thinkingMessages.length]);
        msgIndex++;
      }, baseDelay * 0.8);

      timeout = setTimeout(() => {
        clearInterval(thinkInterval);
        setThinkingText('');
        
        // Get a song
        const song = getSongForLetter(currentLetter);
        setCurrentSong(song);
        setPhase('singing');
      }, baseDelay * 2.5);

    } else if (phase === 'singing') {
      // Type out lyrics character by character
      const lyrics = currentSong.lyrics;
      let charIndex = 0;
      
      const typeInterval = setInterval(() => {
        if (charIndex <= lyrics.length) {
          setDisplayedLyrics(lyrics.substring(0, charIndex));
          charIndex++;
        } else {
          clearInterval(typeInterval);
          setPhase('commenting');
        }
      }, 30 / speed);

      return () => clearInterval(typeInterval);

    } else if (phase === 'commenting') {
      timeout = setTimeout(() => {
        // Add the completed song
        const agent = agents[currentAgentIndex];
        const newSong = {
          id: Date.now(),
          agent,
          title: currentSong.title,
          lyrics: currentSong.lyrics,
          startLetter: currentSong.forcedStart || currentLetter,
          endLetter: currentSong.end,
          round: round + 1,
        };
        
        setSongs(prev => [...prev, newSong]);
        
        // Add judge comment
        setTimeout(() => {
          setComments(prev => [...prev, {
            id: Date.now(),
            songId: newSong.id,
            agent: judge,
            text: getRandomItem(judgeComments),
          }]);
        }, baseDelay * 0.5);

        // Add hype comment
        setTimeout(() => {
          setComments(prev => [...prev, {
            id: Date.now() + 1,
            songId: newSong.id,
            agent: hypeboi,
            text: getRandomItem(hypeComments),
          }]);
        }, baseDelay * 1);

        // Move to next round
        setTimeout(() => {
          setCurrentLetter(currentSong.end);
          setCurrentAgentIndex((currentAgentIndex + 1) % agents.length);
          setRound(r => r + 1);
          setCurrentSong(null);
          setDisplayedLyrics('');
          setPhase('thinking');
        }, baseDelay * 2);

      }, baseDelay * 0.5);
    }

    return () => {
      if (timeout) clearTimeout(timeout);
    };
  }, [isPlaying, phase, currentLetter, currentAgentIndex, currentSong, round, speed]);

  const startGame = () => {
    setSongs([]);
    setComments([]);
    setRound(0);
    setCurrentLetter('D');
    setCurrentAgentIndex(0);
    setCurrentSong(null);
    setDisplayedLyrics('');
    setIsPlaying(true);
    setPhase('thinking');
  };

  const stopGame = () => {
    setIsPlaying(false);
    setPhase('idle');
    setThinkingText('');
  };

  const currentAgent = agents[currentAgentIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-1">
            🎤 cagent Antakshari Live 🎵
          </h1>
          <p className="text-gray-500 text-sm">Watch AI Agents Play the Classic Indian Song Game</p>
        </div>

        {/* Agent Roster */}
        <div className="bg-white rounded-xl p-4 mb-4 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex gap-2 flex-wrap">
              {agents.map((agent, i) => (
                <div
                  key={agent.id}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm transition-all ${
                    isPlaying && currentAgentIndex === i
                      ? `${agent.color} text-white scale-110 shadow-lg`
                      : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  <span>{agent.emoji}</span>
                  <span className="font-medium">{agent.name}</span>
                  {isPlaying && currentAgentIndex === i && (
                    <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                  )}
                </div>
              ))}
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-2 py-1 rounded text-xs ${judge.color} text-white`}>{judge.emoji} Judge</span>
              <span className={`px-2 py-1 rounded text-xs ${hypeboi.color} text-white`}>{hypeboi.emoji} Hype</span>
            </div>
          </div>
        </div>

        {/* Game Status Bar */}
        <div className="bg-white rounded-xl p-4 mb-4 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="text-center">
                <div className="text-xs text-gray-500 uppercase tracking-wide">Round</div>
                <div className="text-2xl font-bold text-purple-600">{round}</div>
              </div>
              <div className="text-center">
                <div className="text-xs text-gray-500 uppercase tracking-wide">Current Letter</div>
                <div className="text-4xl font-bold text-yellow-500">{currentLetter}</div>
              </div>
              <div className="text-center">
                <div className="text-xs text-gray-500 uppercase tracking-wide">Status</div>
                <div className={`text-sm font-medium ${isPlaying ? 'text-green-500' : 'text-gray-400'}`}>
                  {isPlaying ? '● LIVE' : '○ Paused'}
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              {/* Speed Control */}
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">Speed:</span>
                <select
                  value={speed}
                  onChange={(e) => setSpeed(Number(e.target.value))}
                  className="text-sm border rounded px-2 py-1"
                >
                  <option value={0.5}>0.5x</option>
                  <option value={1}>1x</option>
                  <option value={2}>2x</option>
                  <option value={3}>3x</option>
                </select>
              </div>
              
              {/* Play/Stop Button */}
              {!isPlaying ? (
                <button
                  onClick={startGame}
                  className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-2 rounded-full font-bold hover:opacity-90 transition flex items-center gap-2"
                >
                  <span>▶</span> Start Game
                </button>
              ) : (
                <button
                  onClick={stopGame}
                  className="bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-2 rounded-full font-bold hover:opacity-90 transition flex items-center gap-2"
                >
                  <span>⏹</span> Stop
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Current Action */}
        {isPlaying && phase !== 'idle' && (
          <div className="bg-white rounded-xl p-4 mb-4 shadow-sm border-2 border-purple-300 animate-pulse">
            <div className="flex items-center gap-3">
              <div className={`w-12 h-12 ${currentAgent.color} rounded-full flex items-center justify-center text-2xl text-white`}>
                {currentAgent.emoji}
              </div>
              <div className="flex-1">
                <div className="font-bold text-gray-800">@{currentAgent.name}</div>
                {phase === 'thinking' && (
                  <div className="text-gray-500 text-sm flex items-center gap-2">
                    <span className="flex gap-1">
                      <span className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></span>
                      <span className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></span>
                      <span className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></span>
                    </span>
                    {thinkingText || 'Thinking...'}
                  </div>
                )}
                {phase === 'singing' && currentSong && (
                  <div>
                    <div className="text-purple-600 font-medium">🎵 Singing: "{currentSong.title}"</div>
                    <div className="bg-gray-50 rounded p-3 mt-2 text-sm text-gray-700 whitespace-pre-line border-l-4 border-purple-400">
                      {displayedLyrics}
                      <span className="animate-pulse">|</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Song Feed */}
        <div 
          ref={feedRef}
          className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
          style={{ maxHeight: '500px', overflowY: 'auto' }}
        >
          <div className="sticky top-0 bg-gray-50 px-4 py-2 border-b border-gray-200">
            <span className="font-bold text-gray-700">🎵 Song Feed</span>
            <span className="text-gray-400 text-sm ml-2">({songs.length} songs)</span>
          </div>
          
          <div className="p-4 space-y-4">
            {songs.length === 0 && !isPlaying && (
              <div className="text-center py-12 text-gray-400">
                <div className="text-4xl mb-2">🎤</div>
                <div>Click "Start Game" to watch agents play Antakshari!</div>
              </div>
            )}
            
            {songs.map((song, index) => {
              const songComments = comments.filter(c => c.songId === song.id);
              return (
                <div key={song.id} className="border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                  {/* Song Header */}
                  <div className={`${song.agent.color} px-4 py-2 flex items-center justify-between text-white`}>
                    <div className="flex items-center gap-2">
                      <span className="text-xl">{song.agent.emoji}</span>
                      <span className="font-bold">@{song.agent.name}</span>
                    </div>
                    <span className="text-xs bg-black bg-opacity-20 px-2 py-1 rounded">
                      Round {song.round}
                    </span>
                  </div>
                  
                  {/* Song Content */}
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-bold text-gray-800">"{song.title}"</h3>
                      <div className="flex gap-2">
                        <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded font-medium">
                          {song.startLetter} →
                        </span>
                        <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-medium">
                          → {song.endLetter}
                        </span>
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-700 whitespace-pre-line border-l-4 border-purple-400">
                      {song.lyrics}
                    </div>
                    
                    {/* Comments */}
                    {songComments.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-100 space-y-2">
                        {songComments.map(comment => (
                          <div key={comment.id} className="flex gap-2 text-sm">
                            <span>{comment.agent.emoji}</span>
                            <span className="font-bold text-gray-700">@{comment.agent.name}:</span>
                            <span className="text-gray-600">{comment.text}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Letter Chain Visualization */}
        {songs.length > 0 && (
          <div className="mt-4 bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="text-xs text-gray-500 uppercase tracking-wide mb-2">Letter Chain</div>
            <div className="flex flex-wrap items-center gap-1">
              {songs.map((song, i) => (
                <React.Fragment key={song.id}>
                  <span className={`${song.agent.color} text-white px-2 py-1 rounded text-sm font-bold`}>
                    {song.startLetter}
                  </span>
                  <span className="text-gray-400">→</span>
                  {i === songs.length - 1 && (
                    <span className="bg-yellow-100 text-yellow-700 px-2 py-1 rounded text-sm font-bold animate-pulse">
                      {song.endLetter}?
                    </span>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-6 text-gray-400 text-sm">
          <p>Powered by Docker cagent | Built by Collabnix Community</p>
          <p className="mt-1">🐳 github.com/ajeetraina/docker-cagent-antakshari</p>
        </div>
      </div>
    </div>
  );
}
