(function() {
    (function(a) {
        "use strict";
        var b = Function.prototype.call.bind(Function.prototype.toString);
        var c = [];
        var d = [];
        var e = {
            toString: function() {
                var f = c.lastIndexOf(this);
                if (f >= 0) {
                    return d[f]
                }
                return b(this)
            }
        };
        e.toString.prototype = void 0;
        c = [e.toString];
        d = [b(Function.prototype.toString)];
        function g(h, i) {
            if (typeof i !== "function") {
                return
            }
            try {
                var j = e.toString.call(i);
                d.push(j);
                c.push(h);
                if (Function.prototype.toString !== e.toString) {
                    Function.prototype.toString = e.toString
                }
            } catch (k) {}
        }
        var l = "ZT4tcOwEFkVEzfiT1T6u";
        var m = Object.call.bind(Object.bind, Object.call);
        var n = m(Object.call);
        var o = Array.prototype.push;
        var p = Array.prototype.indexOf;
        var q = Array.prototype.concat;
        var r = Array.prototype.slice;
        function s() {
            return {
                __callbacks: [],
                notify: function(t) {
                    var u;
                    var v = n(r, this.__callbacks);
                    var w = v.length;
                    for (var x = w - 1; x >= 0; --x) {
                        try {
                            var y = v[x];
                            if (y != null) {
                                var z = y(t, u);
                                if (z != null) {
                                    u = z
                                }
                            }
                        } catch (A) {}
                    }
                    return u
                },
                register: function(B) {
                    n(o, this.__callbacks, B)
                },
                unregister: function(C) {
                    var D = n(p, this.__callbacks, C);
                    if (D !== -1) {
                        this.__callbacks[D] = null
                    }
                },
                __merge: function(E) {
                    if (E != null) {
                        this.__callbacks = n(q, this.__callbacks, E.__callbacks)
                    }
                }
            }
        }
        var F = Object.hasOwnProperty;
        var G = Object.getPrototypeOf;
        var H = Object.getOwnPropertyDescriptor;
        var I = Object.getOwnPropertyNames;
        var J = Object.defineProperty;
        var K = Object.call.bind(Object.bind, Object.call);
        var L = K(Object.apply);
        var M = K(Object.call);
        var N = Object.create;
        var O = Function.prototype.bind;
        var P = Array.prototype.push;
        var Q = Array.prototype.indexOf;
        var R = ["arguments", "caller"];
        var S;
        if (typeof Reflect !== "undefined" && Reflect != null && typeof Reflect.construct === "function") {
            S = Reflect.construct
        } else {
            S = function(T, U) {
                var V = [null];
                L(P, V, U);
                var W = L(O, T, V);
                return new W
            }
        }
        function X(Y, Z) {
            var ba = Y;
            while (ba != null) {
                var bb = H(ba, Z);
                if (bb != null) {
                    return {
                        containingObj: ba,
                        desc: bb
                    }
                }
                ba = G(ba)
            }
            return null
        }
        var bc = N(null);
        function bd(be) {
            if (be == null) {
                return
            }
            bc = be
        }
        function bf(bg, bh) {
            var bi = bc[bh];
            if (bi == null) {
                return null
            }
            for (var bj = 0; bj < bi.length; ++bj) {
                var bk = bi[bj];
                if (bg === bk.object) {
                    return bk
                }
            }
            return null
        }
        function bl(bm, bn) {
            var bo = bc[bm];
            if (bo == null) {
                bo = [];
                bc[bm] = bo
            }
            M(P, bo, bn)
        }
        function bp(bq, br) {
            var bs = X(bq, br);
            if (bs == null) {
                return void 0
            }
            var bt = bs.containingObj
              , bu = bs.desc;
            var bv = bf(bt, br);
            if (bv != null) {
                return bv.original
            }
            var bw = bu.value;
            bl(br, {
                object: bt,
                original: bw
            });
            return bw
        }
        function bx(by, bz) {
            var bA = X(by, bz);
            if (bA == null) {
                return void 0
            }
            var bB = bA.containingObj
              , bC = bA.desc;
            var bD = bf(bB, bz);
            if (bD != null) {
                return bD.original
            }
            if (M(F, bC, "value")) {
                return void 0
            }
            var bE = N(null);
            if (bC.get != null) {
                bE.get = bC.get
            }
            if (bC.set != null) {
                bE.set = bC.set
            }
            bl(bz, {
                object: bB,
                original: bE
            });
            return bE
        }
        function bF(bG, bH, bI) {
            if (bI === void 0) {
                bI = false
            }
            var bJ = X(bG, bH);
            if (bJ == null) {
                return null
            }
            var bK = bJ.containingObj
              , bL = bJ.desc;
            var bM = bL.configurable
              , bN = bL.writable;
            var bO = bL.value;
            if (!M(F, bL, "value")) {
                return null
            }
            var bP = N(null);
            bP.value = bO;
            if (bM === false && bN === false || typeof bO !== "function") {
                return {
                    originals: bP
                }
            }
            var bQ = bf(bK, bH);
            if (bQ != null) {
                if (bQ.result != null) {
                    return bQ.result
                }
                bO = bQ.original;
                bP.value = bO
            }
            var bR = s();
            var bS = s();
            bL.value = function bT() {
                var bU = arguments;
                var bV = bR.notify({
                    args: bU,
                    thisObj: this
                });
                if (bV) {
                    if (bV.bypassResult != null) {
                        if (bV.bypassResult.throw) {
                            throw bV.bypassResult.value
                        }
                        return bV.bypassResult.value
                    } else if (bV.args != null) {
                        bU = bV.args
                    }
                }
                var bW;
                var bX = {
                    args: arguments,
                    thisObj: this,
                    threw: true,
                    result: null
                };
                try {
                    if (bI && this instanceof bT) {
                        bW = S(bO, bU)
                    } else {
                        bW = L(bO, this, bU)
                    }
                    bX = {
                        args: arguments,
                        thisObj: this,
                        threw: false,
                        result: bW
                    }
                } finally {
                    var bY = bS.notify(bX);
                    if (bY && bY.bypassResult != null) {
                        if (bY.bypassResult.throw) {
                            throw bY.bypassResult.value
                        }
                        return bY.bypassResult.value
                    }
                }
                return bW
            }
            ;
            var bZ = bL.value;
            g(bZ, bO);
            var ca = I(bO);
            for (var cb = 0; cb < ca.length; ++cb) {
                var cc = ca[cb];
                if (M(Q, R, cc) === -1) {
                    var cd = H(bZ, cc);
                    if (cd == null || cd.configurable === true || cd.writable === true) {
                        var ce = H(bO, cc);
                        if (ce != null) {
                            if (cd != null && cd.configurable === false && ce.configurable === true) {} else {
                                J(bZ, cc, ce)
                            }
                        }
                    }
                }
            }
            try {
                if (!M(F, bO, "prototype")) {
                    bZ.prototype = void 0
                }
            } catch (cf) {}
            J(bK, bH, bL);
            var cg = {
                onBeforeInvoke: bR,
                onAfterInvoke: bS,
                originals: bP
            };
            bl(bH, {
                object: bK,
                result: cg,
                original: bO
            });
            return cg
        }
        function ch(ci, cj) {
            var ck = X(ci, cj);
            if (ck == null) {
                return null
            }
            var cl = ck.containingObj
              , cm = ck.desc;
            var cn = cm.configurable;
            var co = cm
              , cp = co.get
              , cq = co.set;
            var cr = M(F, cm, "value");
            var cs = N(null);
            if (cn === false || cr) {
                if (cp != null) {
                    cs.get = cp
                }
                if (cq != null) {
                    cs.set = cq
                }
                return {
                    originals: cs
                }
            }
            var ct = bf(cl, cj);
            if (ct != null) {
                if (ct.result != null) {
                    return ct.result
                }
                cp = ct.original.get;
                cq = ct.original.set
            }
            var cu = {
                onAfterGet: void 0,
                onBeforeGet: void 0,
                onAfterSet: void 0,
                onBeforeSet: void 0,
                originals: {}
            };
            if (cp != null) {
                cs.get = cp;
                var cv = s();
                var cw = s();
                cm.get = function() {
                    var cx = cv.notify({
                        thisObj: this
                    });
                    if (cx && cx.bypassResult != null) {
                        if (cx.bypassResult.throw) {
                            throw cx.bypassResult.value
                        }
                        return cx.bypassResult.value
                    }
                    var cy;
                    var cz = {
                        thisObj: this,
                        result: null,
                        threw: true
                    };
                    try {
                        cy = M(cp, this);
                        cz = {
                            thisObj: this,
                            result: cy,
                            threw: false
                        }
                    } finally {
                        var cA = cw.notify(cz);
                        if (cA && cA.bypassResult != null) {
                            if (cA.bypassResult.throw) {
                                throw cA.bypassResult.value
                            }
                            return cA.bypassResult.value
                        }
                    }
                    return cy
                }
                ;
                g(cm.get, cp);
                try {
                    if (!M(F, cp, "prototype")) {
                        cm.get.prototype = void 0
                    }
                } catch (cB) {}
                cu.onBeforeGet = cv;
                cu.onAfterGet = cw
            }
            if (cq != null) {
                cs.set = cq;
                var cC = s();
                var cD = s();
                cm.set = function(cE) {
                    var cF = cE;
                    var cG = cC.notify({
                        param: cE,
                        thisObj: this
                    });
                    if (cG) {
                        if (cG.bypassResult != null) {
                            if (cG.bypassResult.throw) {
                                throw cG.bypassResult.value
                            }
                            return cG.bypassResult.value
                        } else if (M(F, cG, "param")) {
                            cF = cG.param
                        }
                    }
                    var cH;
                    var cI = {
                        param: cE,
                        thisObj: this,
                        result: null,
                        threw: true
                    };
                    try {
                        cH = M(cq, this, cF);
                        cI = {
                            param: cE,
                            thisObj: this,
                            result: cH,
                            threw: false
                        }
                    } finally {
                        var cJ = cD.notify(cI);
                        if (cJ && cJ.bypassResult != null) {
                            if (cJ.bypassResult.throw) {
                                throw cJ.bypassResult.value
                            }
                            return cJ.bypassResult.value
                        }
                    }
                    return cH
                }
                ;
                g(cm.set, cq);
                try {
                    if (!M(F, cq, "prototype")) {
                        cm.set.prototype = void 0
                    }
                } catch (cK) {}
                cu.onBeforeSet = cC;
                cu.onAfterSet = cD
            }
            J(cl, cj, cm);
            cu.originals = cs;
            bl(cj, {
                object: cl,
                result: cu,
                original: cs
            });
            return cu
        }
        try {
            if (typeof document.createEvent === "function") {
                var cL = document.createEvent("CustomEvent");
                var cM = false;
                cL.initCustomEvent(l, false, false, {
                    exchange: function(cN) {
                        bd(cN);
                        cM = true
                    }
                });
                dispatchEvent(cL);
                if (!cM) {
                    var cO = bx(CustomEvent.prototype, "detail");
                    if (cO != null && typeof cO.get === "function") {
                        addEventListener(l, function(cP) {
                            var cQ = cP;
                            var cR = M(cO.get, cQ);
                            if (cR != null && typeof cR.exchange === "function") {
                                cR.exchange(bc)
                            }
                        })
                    }
                }
            }
        } catch (cS) {}
        var cT = Object.create(null);
        var cU = Object.create(null);
        {
            var cV = "\u202EKDQZPCCsH\u202D";
            var cW = XMLHttpRequest;
            var cX;
            var cY
        }
        {
            var cZ = window.fetch;
            var da
        }
        var db = "\u202EduIZWEoPX\u202D";
        var dc = "-2\u202EduIZWEoPX\u202D";
        var dd = void 0;
        var de = Object.defineProperty.bind(Object);
        function df(dg, dh, di, dj, dk) {
            if (dj === "function") {
                cT[dg] = bF(dl(di), dh, !!dk)
            } else if (dj === "accessor") {
                cT[dg] = ch(dl(di), dh)
            } else if (dj === "originalAccessor") {
                cU[dg] = bx(dl(di), dh)
            } else if (dj === "originalFunction") {
                cU[dg] = bp(dl(di), dh)
            }
        }
        function dl(dm) {
            var dn = window;
            for (var dp = 0; dp < dm.length; dp++) {
                if (!{}.hasOwnProperty.call(dn, dm[dp])) {
                    return void 0
                }
                dn = dn[dm[dp]]
            }
            return dn
        }
        df("CustomEvent", "CustomEvent", [], "function", true);
        df("cancelBubble", "cancelBubble", ["Event", "prototype"], "accessor");
        df("fetch", "fetch", [], "function");
        df("formSubmit", "submit", ["HTMLFormElement", "prototype"], "function");
        df("preventDefault", "preventDefault", ["Event", "prototype"], "function");
        df("setRequestHeader", "setRequestHeader", ["XMLHttpRequest", "prototype"], "originalFunction");
        df("stopImmediatePropagation", "stopImmediatePropagation", ["Event", "prototype"], "function");
        df("stopPropagation", "stopPropagation", ["Event", "prototype"], "function");
        df("xhrOpen", "open", ["XMLHttpRequest", "prototype"], "function");
        df("xhrSend", "send", ["XMLHttpRequest", "prototype"], "function");
        (function() {
            if (cW == null) {
                return
            }
            var dq = cU.setRequestHeader != null ? cU.setRequestHeader : cT.setRequestHeader != null ? cT.setRequestHeader.originals.value : null;
            if (dq == null) {
                return
            }
            if (cT.xhrOpen != null) {
                cX = function(dr, ds) {
                    if (ds != null && ds.bypassResult != null || dr.args == null || dr.args.length < 2) {
                        return ds
                    }
                    var dt, du = null;
                    var dv;
                    var dw = ds != null && ds.args != null ? ds.args : dr.args;
                    var dt = dw[0];
                    var du = dw[1];
                    var dv = dw[2] == null ? true : dw[2];
                    de(dr.thisObj, cV, {
                        writable: true,
                        configurable: true,
                        enumerable: false,
                        value: {
                            method: dt,
                            url: du
                        }
                    });
                    return {
                        args: [dt, du, dv]
                    }
                }
                ;
                cT.xhrOpen.onBeforeInvoke.register(cX)
            }
            if (cT.xhrSend != null) {
                cY = function(dx, dy) {
                    if (dy != null && dy.bypassResult != null) {
                        return dy
                    }
                    if (dd != null && cV in dx.thisObj && dd.shouldHook(dx.thisObj[cV])) {
                        var dz = dd.getEncodedData();
                        if (dz) {
                            for (var dA in dz) {
                                if (!{}.hasOwnProperty.call(dz, dA))
                                    continue;
                                var dB = dz[dA];
                                var dC = dd.config.headerNamePrefix + dA;
                                var dD = dd.chunk(dC, dB, dd.config.headerChunkSize);
                                for (var dE in dD) {
                                    if (!{}.hasOwnProperty.call(dD, dE))
                                        continue;
                                    dq.call(dx.thisObj, dE, dD[dE])
                                }
                            }
                        }
                    }
                    return dy
                }
                ;
                cT.xhrSend.onBeforeInvoke.register(cY)
            }
        }());
        (function() {
            if (cZ == null) {
                return
            }
            var dF = window.Request;
            if (cT.fetch != null && window.fetch != null && dF != null) {
                var dG = function(dH, dI) {
                    var dJ = dH.args;
                    if (dI != null) {
                        if (dI.bypassResult != null) {
                            return dI
                        }
                        if (dI.args != null) {
                            dJ = dI.args
                        }
                    }
                    if (dJ != null && dJ.length > 0) {
                        var dK = dJ[0];
                        var dL = dJ[1];
                        var dM = new dF(dK,dL);
                        var dN = {
                            url: dM.url,
                            method: dM.method
                        };
                        if (dd != null && dd.shouldHook(dN)) {
                            var dO = dd.getEncodedData();
                            if (dO) {
                                for (var dP in dO) {
                                    if (!{}.hasOwnProperty.call(dO, dP))
                                        continue;
                                    var dQ = dO[dP];
                                    var dR = dd.config.headerNamePrefix + dP;
                                    var dS = dd.chunk(dR, dQ, dd.config.headerChunkSize);
                                    for (var dT in dS) {
                                        if (!{}.hasOwnProperty.call(dS, dT))
                                            continue;
                                        dM.headers.set(dT, dS[dT])
                                    }
                                }
                            }
                        }
                        return {
                            args: [dM]
                        }
                    }
                    return dI
                };
                cT.fetch.onBeforeInvoke.register(dG)
            }
        }());
        addEventListener(db, function dU(dV) {
            dd = dV.detail;
            removeEventListener(db, dU, true)
        }, true);
        addEventListener(dc, function dW(dX) {
            if (dX.detail != null && dX.detail.exchange != null) {
                {
                    if (cT.xhrOpen != null && cX != null) {
                        cT.xhrOpen.onBeforeInvoke.unregister(cX)
                    }
                    if (cT.xhrSend != null && cY != null) {
                        cT.xhrSend.onBeforeInvoke.unregister(cY)
                    }
                }
                {
                    if (cT.fetch != null) {
                        cT.fetch.onBeforeInvoke.unregister(da)
                    }
                }
                dX.detail.exchange({
                    instrumented: cT
                })
            }
            removeEventListener(dc, dW, true)
        }, true)
    }(this))
}())
