(function (a, d, p) { a.fn.backstretch = function (c, b) { (c === p || 0 === c.length) && a.error("No images were supplied for Backstretch"); 0 === a(d).scrollTop() && d.scrollTo(0, 0); return this.each(function () { var d = a(this), g = d.data("backstretch"); if (g) { if ("string" == typeof c && "function" == typeof g[c]) { g[c](b); return } b = a.extend(g.options, b); g.destroy(!0) } g = new q(this, c, b); d.data("backstretch", g) }) }; a.backstretch = function (c, b) { return a("body").backstretch(c, b).data("backstretch") }; a.expr[":"].backstretch = function (c) { return a(c).data("backstretch") !== p }; a.fn.backstretch.defaults = { centeredX: !0, centeredY: !0, duration: 5E3, fade: 0 }; var r = { left: 0, top: 0, overflow: "hidden", margin: 0, padding: 0, height: "100%", width: "100%", zIndex: -999999 }, s = { position: "absolute", display: "none", margin: 0, padding: 0, border: "none", width: "auto", height: "auto", maxHeight: "none", maxWidth: "none", zIndex: -999999 }, q = function (c, b, e) { this.options = a.extend({}, a.fn.backstretch.defaults, e || {}); this.images = a.isArray(b) ? b : [b]; a.each(this.images, function () { a("<img />")[0].src = this }); this.isBody = c === document.body; this.$container = a(c); this.$root = this.isBody ? l ? a(d) : a(document) : this.$container; c = this.$container.children(".backstretch").first(); this.$wrap = c.length ? c : a('<div class="backstretch"></div>').css(r).appendTo(this.$container); this.isBody || (c = this.$container.css("position"), b = this.$container.css("zIndex"), this.$container.css({ position: "static" === c ? "relative" : c, zIndex: "auto" === b ? 0 : b, background: "none" }), this.$wrap.css({ zIndex: -999998 })); this.$wrap.css({ position: this.isBody && l ? "fixed" : "absolute" }); this.index = 0; this.show(this.index); a(d).on("resize.backstretch", a.proxy(this.resize, this)).on("orientationchange.backstretch", a.proxy(function () { this.isBody && 0 === d.pageYOffset && (d.scrollTo(0, 1), this.resize()) }, this)) }; q.prototype = { resize: function () { try { var a = { left: 0, top: 0 }, b = this.isBody ? this.$root.width() : this.$root.innerWidth(), e = b, g = this.isBody ? d.innerHeight ? d.innerHeight : this.$root.height() : this.$root.innerHeight(), j = e / this.$img.data("ratio"), f; j >= g ? (f = (j - g) / 2, this.options.centeredY && (a.top = "-" + f + "px")) : (j = g, e = j * this.$img.data("ratio"), f = (e - b) / 2, this.options.centeredX && (a.left = "-" + f + "px")); this.$wrap.css({ width: b, height: g }).find("img:not(.deleteable)").css({ width: e, height: j }).css(a) } catch (h) { } return this }, show: function (c) { if (!(Math.abs(c) > this.images.length - 1)) { var b = this, e = b.$wrap.find("img").addClass("deleteable"), d = { relatedTarget: b.$container[0] }; b.$container.trigger(a.Event("backstretch.before", d), [b, c]); this.index = c; clearInterval(b.interval); b.$img = a("<img />").css(s).bind("load", function (f) { var h = this.width || a(f.target).width(); f = this.height || a(f.target).height(); a(this).data("ratio", h / f); a(this).fadeIn(b.options.speed || b.options.fade, function () { e.remove(); b.paused || b.cycle(); a(["after", "show"]).each(function () { b.$container.trigger(a.Event("backstretch." + this, d), [b, c]) }) }); b.resize() }).appendTo(b.$wrap); b.$img.attr("src", b.images[c]); return b } }, next: function () { return this.show(this.index < this.images.length - 1 ? this.index + 1 : 0) }, prev: function () { return this.show(0 === this.index ? this.images.length - 1 : this.index - 1) }, pause: function () { this.paused = !0; return this }, resume: function () { this.paused = !1; this.next(); return this }, cycle: function () { 1 < this.images.length && (clearInterval(this.interval), this.interval = setInterval(a.proxy(function () { this.paused || this.next() }, this), this.options.duration)); return this }, destroy: function (c) { a(d).off("resize.backstretch orientationchange.backstretch"); clearInterval(this.interval); c || this.$wrap.remove(); this.$container.removeData("backstretch") } }; var l, f = navigator.userAgent, m = navigator.platform, e = f.match(/AppleWebKit\/([0-9]+)/), e = !!e && e[1], h = f.match(/Fennec\/([0-9]+)/), h = !!h && h[1], n = f.match(/Opera Mobi\/([0-9]+)/), t = !!n && n[1], k = f.match(/MSIE ([0-9]+)/), k = !!k && k[1]; l = !((-1 < m.indexOf("iPhone") || -1 < m.indexOf("iPad") || -1 < m.indexOf("iPod")) && e && 534 > e || d.operamini && "[object OperaMini]" === {}.toString.call(d.operamini) || n && 7458 > t || -1 < f.indexOf("Android") && e && 533 > e || h && 6 > h || "palmGetResource" in d && e && 534 > e || -1 < f.indexOf("MeeGo") && -1 < f.indexOf("NokiaBrowser/8.5.0") || k && 6 >= k) })(jQuery, window);

$("body.modal").backstretch(
    [
        "https://s3.amazonaws.com/SSL_Assets/Adelaide/Styles/Headers/slide02.jpg"
        , "https://s3.amazonaws.com/SSL_Assets/Adelaide/Styles/Headers/slide03.jpg"
        , "https://s3.amazonaws.com/SSL_Assets/Adelaide/Styles/Headers/slide04.jpg"
    ], { duration: 3000, fade: 750 });

//$("#forgot_password_instructions").text("Enter your Selwyn Email and we will send you a link to your password.");

// UOFA : INSERT CUSTOM SCRIPTS BELOW

$("#dashboard-activity")
    .before(
        '<div style="font-size: 16px; font-weight: bold;">Your <a href="https://access.adelaide.edu.au/" target="_blank">enrolled courses</a> appear here once published by your course coordinator.<br/>' +
        'Use Turnitin to <a href="https://myuni.adelaide.edu.au/search/all_courses/" target="_blank">check the originality</a> of your draft assignments.</div>'
    );

// UOFA JIRA MUT-455 : Disable end user ability to change default email address (Chetan)
$(".channel:not(.default)>.email_meta").html("");

// UOFA JIRA MUT-483 : Maintaining email configuration in Canvas
$("select#default_email_id option:not(:selected)").remove();

// UOFA JIRA MUT-200 : TAT Google Analytics Code (Chetan)
(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date(); a = s.createElement(o),
        m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-15181647-9', 'auto', 'uofa');
ga('uofa.send', 'pageview');

// UOFA JIRA AAD-198 : Custom footer links
var copyrightLink = '<a href="https://www.adelaide.edu.au/library/copyright/" target="_blank">Copyright</a>';

var touLink = '<a href="https://www.canvaslms.com/policies/intl-terms-of-use" target="_blank">Terms of Use</a>';

var securityLink = '<a href="https://www.adelaide.edu.au/policies/2783/" target="_blank">IT Acceptable Use and Security Policy</a>';

var privacyLink = '<a href="https://www.adelaide.edu.au/policies/62/" target="_blank">Privacy</a>';

$('<div class="ic-app-footer ic-app-footer__links">' + copyrightLink + touLink + securityLink + privacyLink + '</div>').insertBefore('#footer');

// UOFA JIRA AAD-303 : Code Highlighting
(window.Prism = window.Prism || {}).manual = true; // Disable autohighlighting
$("pre[class^='lang'], pre[class^=' lang']").addClass("line-numbers"); // Add CSS class to generate line numbers

var prismScriptsBase = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.14.0/";
var prismScripts = [
    "components/prism-markup-templating.min.js",
    "components/prism-clike.min.js",
    "components/prism-c.min.js",
    "components/prism-csharp.min.js",
    "components/prism-cpp.min.js",
    "components/prism-css.min.js",
    "components/prism-fsharp.min.js",
    "components/prism-java.min.js",
    "components/prism-markup.min.js",
    "components/prism-javascript.min.js",
    "components/prism-json.min.js",
    "components/prism-less.min.js",
    "components/prism-php.min.js",
    "components/prism-processing.min.js",
    "components/prism-python.min.js",
    "components/prism-ruby.min.js",
    "components/prism-sass.min.js",
    "components/prism-sql.min.js",
    "components/prism-typescript.min.js",
    "plugins/line-numbers/prism-line-numbers.js"
];

// Load Script and return promise
function loadScript(script) {
    return $.getScript(script);
}
// Load list of scripts
function loadScripts(scripts) {
    // Reduce, causes sequenctial order of execution
    return scripts.reduce(function (promise, script) {
        // When promise is complete, load next script
        return promise.then(function () {
            return loadScript(prismScriptsBase + script);
        });
    }, $().promise());
}

// Synchronously load Prism, language components and line numbers plugin, highlight code
$.getScript(prismScriptsBase + "prism.min.js", function () {
    loadScripts(prismScripts).then(function () {
        window.onload = function () { Prism.highlightAll(); };
    });
});

// Add needed CSS files
$("head").append('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.14.0/themes/prism.min.css">');
$("head").append('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.14.0/plugins/line-numbers/prism-line-numbers.css">');

var url = window.location.href;

var target = document.getElementById("content");
var codesampleApplied = [];

var observer = new MutationObserver(function () {
    if (typeof tinymce !== "undefined") {
        tinymce.baseURL = "https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.7.13/"; // Set a new base URL, we can't use Instructure's
        $("head").append('<style>.mce-i-codesample:before{content:"Code";}</style>'); // Toolbar access via "Code"

        // Attach plugin and add a toolbar entry
        var pluginApplied = false;
        var toolbarApplied = false;
        if (typeof tinymce.settings.external_plugins !== "undefined") {
            if (!('codesample' in tinymce.settings.external_plugins)) {
                tinymce.settings.external_plugins['codesample'] = 'plugins/codesample/plugin.min.js';
                tinymce.settings.codesample_languages = [
                    { text: 'C', value: 'c' },
                    { text: 'C#', value: 'csharp' },
                    { text: 'C++', value: 'cpp' },
                    { text: 'CSS', value: 'css' },
                    { text: 'F#', value: 'fsharp' },
                    { text: 'HTML/XML', value: 'markup' },
                    { text: 'Java', value: 'java' },
                    { text: 'JavaScript', value: 'javascript' },
                    { text: 'Json', value: 'json' },
                    { text: 'LESS', value: 'less' },
                    { text: 'PHP', value: 'php' },
                    { text: 'Processing', value: 'processing' },
                    { text: 'Python', value: 'python' },
                    { text: 'Ruby', value: 'ruby' },
                    { text: 'SASS', value: 'scss' },
                    { text: 'SQL', value: 'sql' },
                    { text: 'TypeScript', value: 'typescript' }
                ]
            }
            pluginApplied = true;
        }
        if (typeof tinymce.settings.toolbar !== "undefined") {
            if (tinymce.settings.toolbar[0].indexOf(' codesample') == -1) {
                tinymce.settings.toolbar[0] += ' codesample';
            }
            toolbarApplied = true;
        }

        if (pluginApplied && toolbarApplied) {
            // Since Canvas creates the tinymce editor without codesample we've to remove and re-add them
            tinymce.EditorManager.editors.forEach(function (editor) {
                if (codesampleApplied.includes(editor.id)) {
                    return;
                }
                codesampleApplied.push(editor.id);
                editor.on("init", function () {
                    tinymce.EditorManager.execCommand('mceRemoveEditor', false, editor.id);
                    tinymce.EditorManager.execCommand('mceAddEditor', false, editor.id);
                });
            });
        }
    }
});

if (target && !url.match(/\/quizzes\//) && !url.match(/\/question_banks\//)) {
  observer.observe(target, { childList: true, subtree: true });
}

////////////////////////////////////////////////////
// Cidilabs DESIGN TOOLS CONFIG AAD-722           //
////////////////////////////////////////////////////
// Copyright (C) 2017  Utah State University
var DT_variables = {
        iframeID: '',
        // Path to the hosted USU Design Tools
        path: 'https://designtools.ciditools.com/',
        templateCourse: '46402',
        // OPTIONAL: Button will be hidden from view until launched using shortcut keys
        hideButton: true,
         // OPTIONAL: Limit by course format
         limitByFormat: false, // Change to true to limit by format
         // adjust the formats as needed. Format must be set for the course and in this array for tools to load
         formatArray: [
            'online',
            'on-campus',
            'blended'
        ],
        // OPTIONAL: Limit tools loading by users role
        limitByRole: false, // set to true to limit to roles in the roleArray
        // adjust roles as needed
        roleArray: [
            'student',
            'teacher',
            'admin'
        ],
        // OPTIONAL: Limit tools to an array of Canvas user IDs
        limitByUser: false, // Change to true to limit by user
        // add users to array (Canvas user ID not SIS user ID)
        userArray: [
            '1234',
            '987654'
        ]
};

// Run the necessary code when a page loads
$(document).ready(function () {
    'use strict';
    // This runs code that looks at each page and determines what controls to create
    $.getScript(DT_variables.path + 'js/master_controls.js', function () {
        console.log('master_controls.js loaded');
    });
});
////////////////////////////////////////////////////
// END DESIGN TOOLS CONFIG                        //
////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////
//DATACAMP LIGHT IMPLEMENTATION FOR PEARSON PYTHON COURSES //
////////////////////////////////////////////////////////////

// add the Datacamp Light JS (to allow inline instances)
var dclScript = document.createElement("script");
dclScript.src = 'https://cdn.datacamp.com/dcl-react.js.gz'; // 'all new version'
//dclScript.src = 'https://cdn.datacamp.com/datacamp-light-latest.min.js'; // 'old version'
dclScript.type = 'text/javascript';
dclScript.onload = function() {
	console.log('Datacamp Light JS loaded');
};
document.body.appendChild(dclScript);


// set the keyboard keys to use for the shortcuts (using the 'accesskey' attribute)
var exitAccessKey = '2';
var runAccessKey = '1';

// set up a mutation observer to see when the cursor appears within a DCL instance (i.e. when the editor becomes active)
var cursorObserver = new MutationObserver(function(mutations) {
	if($('.ace_cursor-layer').not('.ace_hidden-cursors').length > 0) {
		var dclInstance = $('.ace_cursor-layer').not('.ace_hidden-cursors').eq(0).closest('.datacamp-exercise');

		if(dclInstance.length > 0) {
			// flag which editor is the current one (remains 'current' until another instance becomes active)
			$('.datacamp-exercise').not(dclInstance).removeClass('current-editor');
			dclInstance.addClass('current-editor');

			// this editor is active, so move the exit point to before this instance & set its accesskey
			dclInstance.before($('.dcl-exit-point'));
			$('.dcl-exit-point').attr('accesskey', exitAccessKey);

			// remove any previous 'run' shortcut, and apply it to this DCL instance
			$('button[class*="Button-module__primary"]').removeAttr('accesskey');
			$('button[class*="Button-module__primary"]', dclInstance).attr('accesskey', runAccessKey);
		}
	} else {
		// remove the accesskey (shortcut) for the exit as there's no active editor
		$('.dcl-exit-point').removeAttr('accesskey');
	}
});
var cursorObserverConfig = { attributes: true, childList: false, subtree: false	};

// set up a mutation observer for when content has been added to the page (to check if a Datacamp Light instance has been added)
var dclObserver = new MutationObserver(function(mutations) {
	if($('.datacamp-exercise').length > 0) {
		// add an exit point to get out of DCL via the keyboard (only one is needed on the page)
		if($('.dcl-exit-point').length == 0) {
			$('h1.page-title').after('<a href="#" class="dcl-exit-point sr-only" accesskey="'+exitAccessKey+'">Code editor exit point</a>');
			$('.dcl-exit-point').click(function(e) { e.preventDefault(); })
		}

		var numDCLSetUp = 0;
		$('.datacamp-exercise').each(function(index) {
			// check if instance has been initialised
			if($('.ace_text-input', $(this)).length > 0) {
				if($('.dcl-skip-link', $(this)).length == 0) {
					numDCLSetUp++;

					$(this)
						.prepend('<a class="dcl-skip-link sr-only" href="#editor'+index+'">Skip over code editor</a>')
						.append('<a name="editor'+index+'" id="editor'+index+'"></a>');

					// remove any previous 'run' shortcut, and apply it to this DCL instance
					$('button[class*="Button-module__primary"]').removeAttr('accesskey');
					$('button[class*="Button-module__primary"]', $(this)).attr('accesskey', runAccessKey);

					// add the cursor mutation observer to this instance of DCL
					$('.ace_cursor-layer', $(this)).each(function(index) {
						cursorObserver.observe($(this)[0], cursorObserverConfig);
					})
				}
			}
		})

		if(numDCLSetUp == $('.datacamp-exercise').length) dclObserver.disconnect();
	}
});
var dclObserverConfig = { attributes: false, childList: true, subtree: true };
dclObserver.observe($('body')[0], dclObserverConfig);

/////////////////////////////////////////////////////////////
// END DATACAMP LIGHT IMPLEMENTATION                      //
///////////////////////////////////////////////////////////

// H5P TOOL CONFIG AAD-722 : adjust the size of the content in iframe
var h5pScript = document.createElement('script');
h5pScript.setAttribute('charset', 'UTF-8');
h5pScript.setAttribute('src', 'https://h5p.org/sites/all/modules/h5p/library/js/h5p-resizer.js');
document.body.appendChild(h5pScript);

// AAD-1082 Installation of Atomic Search
var atomicSearchConfig = {
    accountId: 1,
    externalToolId: 1928,
  };
   
  var atomicSearchWidgetScript = document.createElement("script");
  atomicSearchWidgetScript.src = "https://d2u53n8918fnto.cloudfront.net/atomic_search_widget.js" + "?ts=" + new Date().getTime();
  document.getElementsByTagName("head")[0].appendChild(atomicSearchWidgetScript); 