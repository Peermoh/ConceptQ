      // ---- Market Square (Grade 4) ----
      function () { var g = '<rect x="-62" y="-150" width="124" height="150" fill="#F4E1C1"' + S + '/><path d="M-70 -150 L0 -196 L70 -150 z" fill="#FF7A6B"' + S + '/>';
        for (var c = 0; c < 4; c++) g += '<rect x="' + (-52 + c * 30) + '" y="-136" width="14" height="136" fill="#fff"' + S + '/>';
        g += '<rect x="-48" y="-178" width="96" height="20" rx="4" fill="#fff"' + S + '/>' + txt(0, -164, '1,00,000', 11);
        return g + txt(0, -144, 'TOWN HALL', 10); },
      function () { var g = '<rect x="-64" y="-110" width="128" height="110" fill="#9FE3FF"' + S + '/><path d="M-70 -110 h140 l-10 -18 h-120 z" fill="#5E6B7A"' + S + '/>';
        [-34, 0, 34].forEach(function (x) { g += '<rect x="' + (x - 14) + '" y="-80" width="28" height="80" rx="3" fill="#2A1330"' + S + '/>'; });
        return g + emo(-34, -40, '🚌', 18) + emo(0, -40, '🚌', 18) + emo(34, -40, '🚌', 18) + txt(0, -114, 'BUS DEPOT · 34 × 6', 9, '#fff'); },
      function () { var g = '<rect x="-46" y="-170" width="92" height="170" rx="6" fill="#C88B5A"' + S + '/><path d="M-52 -170 Q0 -214 52 -170 z" fill="#B8F27C"' + S + '/>';
        g += '<rect x="-20" y="-60" width="40" height="60" rx="2" fill="#8A5A3C"' + S + '/>' + emo(0, -120, '🌾', 30);
        return g + txt(0, -78, '744 ÷ 3', 11, '#fff'); },
      function () { var g = shop('#FF8FC7', 'CAKES', ''); g += '<circle cx="0" cy="-58" r="20" fill="#FFF1E2"' + S + '/>';
        for (var i = 0; i < 4; i++) { var a = i / 4 * 6.283; g += '<path d="M0 -58 L' + (Math.cos(a) * 20).toFixed(1) + ' ' + (-58 + Math.sin(a) * 20).toFixed(1) + '" stroke="' + K + '" stroke-width="2"/>'; }
        return g + '<path d="M0 -58 L20 -58 A20 20 0 0 1 0 -38 z" fill="#FF7A6B"/>' + txt(34, -52, '2/4', 12); },
      function () { return shop('#FFD27A', 'TOYS ₹12.50', '🚗🧸🪀'); },
      function () { var g = '<path d="M-34 0 L-20 -120 M34 0 L20 -120 M-30 -40 h60 M-26 -80 h52"' + S + ' fill="none"/>';
        g += '<ellipse cx="0" cy="-150" rx="46" ry="12" fill="#8FD3FF"' + S + '/><rect x="-46" y="-196" width="92" height="46" fill="#8FD3FF"' + S + '/><ellipse cx="0" cy="-196" rx="46" ry="12" fill="#BFE8FF"' + S + '/>';
        return g + txt(0, -170, '1 L = 1000 mL', 10); },
      function () { var g = ''; for (var r = 0; r < 4; r++) for (var c = 0; c < 5; c++) g += '<rect x="' + (-60 + c * 24) + '" y="' + (-28 - r * 24) + '" width="22" height="22" fill="' + ((r + c) % 2 ? '#7CF5C8' : '#5FD39A') + '" stroke="' + K + '" stroke-width="1.2"/>';
        return g + emo(-40, -124, '🌳', 30) + emo(40, -118, '🌳', 24) + txt(0, 16, '4 × 5 = 20 squares', 10, '#FFF6EC'); },
      function () { var g = '<path d="M-22 0 L-10 -150 h20 L22 0 z" fill="#E8C7A0"' + S + '/><g class="spin" style="transform-origin:0px -150px">';
        for (var i = 0; i < 4; i++) g += '<path d="M0 -150 L' + (Math.cos(i * 1.5708) * 62).toFixed(1) + ' ' + (-150 + Math.sin(i * 1.5708) * 62).toFixed(1) + '" stroke="#C3A6FF" stroke-width="12" stroke-linecap="round"/>';
        return g + '</g><circle cx="0" cy="-150" r="7" fill="#FFE07A"' + S + '/>' + '<path d="M30 -18 h22 v-22" fill="none" stroke="#FFF6EC" stroke-width="2.5"/>' + txt(0, 16, 'a right angle', 10, '#FFF6EC'); },
      function () { var g = shop('#FFB0D8', 'TILES', ''); for (var r = 0; r < 3; r++) for (var c = 0; c < 4; c++) g += '<rect x="' + (-24 + c * 12) + '" y="' + (-78 + r * 12) + '" width="11" height="11" fill="' + ['#FFC861', '#7CF5C8', '#9FE3FF'][r] + '" stroke="' + K + '" stroke-width="1"/>';
        return g + txt(0, -20, '3 × 4 = 12', 10); },
      function () { var g = '<rect x="-58" y="-140" width="116" height="140" fill="#F4E1C1"' + S + '/><rect x="-48" y="-128" width="96" height="70" rx="4" fill="#fff"' + S + '/>';
        [[-32, 20], [-14, 30], [4, 40], [22, 60]].forEach(function (b) { g += '<rect x="' + (b[0] - 6) + '" y="' + (-62 - b[1] * 0.9) + '" width="14" height="' + (b[1] * 0.9) + '" fill="#9FE3FF" stroke="' + K + '" stroke-width="1.5"/>'; });
        return g + '<rect x="-16" y="-44" width="32" height="44" rx="2" fill="#8A5A3C"' + S + '/>' + txt(0, -146, 'DAILY NEWS', 10, '#FFF6EC'); },
      function () { var g = '<rect x="-60" y="-150" width="120" height="150" fill="#2A1330"' + S + '/><rect x="-52" y="-142" width="104" height="44" rx="4" fill="#FF7A6B"' + S + '/>';
        g += txt(0, -124, 'CINEMA', 13, '#fff') + txt(0, -106, '15:00 · 18:30', 10, '#FFE07A');
        for (var i = 0; i < 8; i++) g += '<circle cx="' + (-52 + i * 14.8) + '" cy="-92" r="3" fill="#FFE07A" class="lamp"/>';
        return g + '<rect x="-20" y="-56" width="40" height="56" rx="2" fill="#8A5A3C"' + S + '/>' + emo(-42, -40, '🎬', 16) + emo(42, -40, '🍿', 16); },
      function () { var g = '<rect x="-24" y="-260" width="48" height="260" fill="#E8C7A0"' + S + '/><path d="M-32 -260 L0 -300 L32 -260 z" fill="#FF7A6B"' + S + '/>';
        g += '<circle cx="0" cy="-226" r="18" fill="#fff"' + S + '/><path d="M0 -226 v-12 M0 -226 h-9" stroke="' + K + '" stroke-width="3" stroke-linecap="round"/>';
        g += '<path d="M-90 -120 Q0 -100 90 -120" fill="none" stroke="' + K + '" stroke-width="2"/>';
        for (var i = 0; i < 7; i++) { var x = -78 + i * 26, y = -118 + Math.sin((i + .5) / 7 * Math.PI) * 14; g += '<path d="M' + (x - 7) + ' ' + y + ' h14 l-7 14 z" fill="' + ['#FFC861', '#7CF5C8', '#FF8FC7', '#9FE3FF', '#C3A6FF', '#B8F27C', '#FFD27A'][i] + '" stroke="' + K + '" stroke-width="1.5"/>'; }
        return g + '<rect x="-12" y="-48" width="24" height="48" rx="12" fill="#8A5A3C"' + S + '/>' + txt(0, 16, 'BIG BAZAAR', 11, '#FFF6EC'); }
