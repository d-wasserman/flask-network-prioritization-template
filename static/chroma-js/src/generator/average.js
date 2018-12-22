const Color = require('../Color');
const {clip_rgb} = require('../utils');
const {pow, sqrt, PI, cos, sin, atan2} = Math;

module.exports = (colors, mode='lrgb') => {
    const l = colors.length;
    // convert colors to Color objects
    colors = colors.map(c => new Color(c));
    if (mode === 'lrgb') {
        return _average_lrgb(colors)
    }
    const first = colors.shift();
    const xyz = first.get(mode);
    const cnt = [];
    let dx = 0;
    let dy = 0;
    // initial color
    for (let i=0; i<xyz.length; i++) {
        xyz[i] = xyz[i] || 0;
        cnt.push(isNaN(xyz[i]) ? 0 : 1);
        if (mode.charAt(i) === 'h' && !isNaN(xyz[i])) {
            const A = xyz[i] / 180 * PI;
            dx += cos(A);
            dy += sin(A);
        }
    }

    let alpha = first.alpha();
    colors.forEach(c => {
        const xyz2 = c.get(mode);
        alpha += c.alpha();
        for (let i=0; i<xyz.length; i++) {
            if (!isNaN(xyz2[i])) {
                cnt[i]++;
                if (mode.charAt(i) === 'h') {
                    const A = xyz2[i] / 180 * PI;
                    dx += cos(A);
                    dy += sin(A);
                } else {
                    xyz[i] += xyz2[i];
                }
            }
        }
    });

    for (let i=0; i<xyz.length; i++) {
        if (mode.charAt(i) === 'h') {
            let A = atan2(dy / cnt[i], dx / cnt[i]) / PI * 180;
            while (A < 0) A += 360;
            while (A >= 360) A -= 360;
            xyz[i] = A;
        } else {
            xyz[i] = xyz[i]/cnt[i];
        }
    }
    alpha /= l;
    return (new Color(xyz, mode)).alpha(alpha > 0.99999 ? 1 : alpha, true);
};


const _average_lrgb = (colors) => {
    const l = colors.length;
    const f = 1/l;
    const xyz = [0,0,0,0];
    for (let col of colors) {
        const rgb = col._rgb;
        xyz[0] += pow(rgb[0],2) * f;
        xyz[1] += pow(rgb[1],2) * f;
        xyz[2] += pow(rgb[2],2) * f;
        xyz[3] += rgb[3] * f;
    }
    xyz[0] = sqrt(xyz[0]);
    xyz[1] = sqrt(xyz[1]);
    xyz[2] = sqrt(xyz[2]);
    if (xyz[3] > 0.9999999) xyz[3] = 1;
    return new Color(clip_rgb(xyz));
}
