var ImageSlide = function(e) {
    this.project = W(e.project),
    this.content = this.project.query(e.content),
    this.tigger = e.tigger ? this.project.query(e.tigger) : null,
    this.watch = e.watch ? this.project.query(e.watch) : null,
    this.dot = e.dot ? this.project.query(e.dot) : null,
    this.isAuto = e.auto || !0,
    this.hide = e.hide && !0,
    this.init()
};
ImageSlide.prototype.init = function() {
    this.register(),
    this.isAuto && this.auto()

},
ImageSlide.prototype.register = function() {
    var e = this;
    this.tigger && this.tigger.forEach(function(t, n) {
        W(t).on("mouseover",
        function() {
            return e.stop(),
            e.show(n),
            !1
        })
    }),
    this.dot && this.dot.forEach(function(t, n) {
        W(t).on("click",
        function() {
            return e.stop(),
            e.show(n),
            !1
        }),
        W(t).on("mouseover",
        function() {
            return e.stop(),
            e.show(n),
            !1
        })
    }),
    this.watch && this.watch.forEach(function(t, n) {
        W(t).on("mouseup",
        function() {
            e.stop(),
            this.className += " down"
        }),
        W(t).on("mousedown",
        function() {
            e.stop(),
            this.className = this.className.replace("down", "")
        }),
        W(t).on("mouseover",
        function() {
            W(this).removeClass("down")
        }),
        W(t).on("mouseout",
        function() {
            W(this).addClass("down")
        }),
        W(t).on("click",
        function() {
            var t = e.index();
            this.className.indexOf("pre") >= 0 && (t = t - 1 < 0 ? e.content.length - 1 : t - 1),
            this.className.indexOf("next") >= 0 && (t = t + 1 > e.content.length - 1 ? 0 : t + 1),
            e.show(t)
        })
    }),
    this.project.on("mouseenter",
    function() {
        //e.tigger && e.hide && e.tigger.css("display", ""),
        //e.watch && e.hide && e.watch.css("display", "inline-block"),
        //e.stop()
    }),
    this.project.on("mouseleave",
    function() {
        //e.tigger && e.hide && e.tigger.css("display", "none"),
        //e.watch && e.hide && e.watch.css("display", "none"),
       // e.auto()
    })
},
ImageSlide.prototype.index = function() {
    var e = 0,
    t = this.content;
    for (var n = 0,
    r = t.length; n < r; n++) t[n].className.indexOf("current") > -1 && (e = n);
    return e
},
ImageSlide.prototype.auto = function() {
    var e = this;
    this.timer = setInterval(function() {
        var t = e.index();
        t = t >= e.content.length - 1 ? 0 : t + 1,
        e.show(t)
    },
    5e3)
},
ImageSlide.prototype.stop = function() {
    this.timer && clearInterval(this.timer)
},
ImageSlide.prototype.show = function(e) {
    this.tigger && this.tigger.addClass && this.tigger.removeClass("current").item(e).addClass("current"),
   // this.dot && this.dot.addClass && this.dot.removeClass("current").item(e).addClass("current"),
    this.content && this.content.addClass && (this.content.filter(".current").removeClass("current"), this.content.item(e).addClass("current"))
};