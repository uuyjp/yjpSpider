function c(t) {
    for (var n = [], i = 0; i < 256; ++i)
        n[i] = (i + 256).toString(16).substr(1);
        var i = 0
          , r = n;
        return [r[t[i++]], r[t[i++]], r[t[i++]], r[t[i++]], "-", r[t[i++]], r[t[i++]], "-", r[t[i++]], r[t[i++]], "-", r[t[i++]], r[t[i++]], "-", r[t[i++]], r[t[i++]], r[t[i++]], r[t[i++]], r[t[i++]], r[t[i++]]].join("")
}
function reqId() {
    var t, e, n
    var r = [
        73,
        113,
        255,
        50,
        29,
        254
    ]
    var o = 7495
    var h = 0, d = 0;

        var i = e && n || 0
          , b = e || []
          , f = (t = t || {}).node || r
          , v = void 0 !== t.clockseq ? t.clockseq : o;
        if (null == f || null == v) {
            var m = l();
            null == f && (f = r = [1 | m[0], m[1], m[2], m[3], m[4], m[5]]),
            null == v && (v = o = 16383 & (m[6] << 8 | m[7]))
        }
        var y = void 0 !== t.msecs ? t.msecs : (new Date).getTime()
          , w = void 0 !== t.nsecs ? t.nsecs : d + 1
          , dt = y - h + (w - d) / 1e4;
        if (dt < 0 && void 0 === t.clockseq && (v = v + 1 & 16383),
        (dt < 0 || y > h) && void 0 === t.nsecs && (w = 0),
        w >= 1e4)
            throw new Error("uuid.v1(): Can't create more than 10M uuids/sec");
        h = y,
        d = w,
        o = v;
        var x = (1e4 * (268435455 & (y += 122192928e5)) + w) % 4294967296;
        b[i++] = x >>> 24 & 255,
        b[i++] = x >>> 16 & 255,
        b[i++] = x >>> 8 & 255,
        b[i++] = 255 & x;
        var _ = y / 4294967296 * 1e4 & 268435455;
        b[i++] = _ >>> 8 & 255,
        b[i++] = 255 & _,
        b[i++] = _ >>> 24 & 15 | 16,
        b[i++] = _ >>> 16 & 255,
        b[i++] = v >>> 8 | 128,
        b[i++] = 255 & v;
        for (var A = 0; A < 6; ++A)
            b[i + A] = f[A];
        return c(b)
}
// console.log(reqId())
// 25750840-3733-11ed-9d47-4971ff321dfe