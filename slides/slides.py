#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import markdown
import base64

class Slides:
    """
    TODO: make a class for one slide with labels etc - compile at the end
    TODO: a slide show is a (possibly nested) list of slides

    """
    def __init__(self, meta):
        self.meta = meta
        # Simply using https://docs.python.org/3.3/library/string.html#format-string-syntax to format strings...
        self.header ="""
<!DOCTYPE html>
<html>
    <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="chrome=1" >
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <meta name="description" content="{title}">
    <meta name="author" content="{author}">

    <meta name="apple-mobile-web-app-capable" content="yes" >
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

    <title>{short_title} - {conference}</title>


    <!-- General and theme style sheets -->
    <link rel="stylesheet" href="{reveal_path}css/reveal.css">
    <link rel="stylesheet" href="{reveal_path}css/theme/{theme}.css" id="theme">
    <!-- Code syntax highlighting -->
    <link rel="stylesheet" href="{reveal_path}lib/css/zenburn.css">
    <!-- Printing and PDF exports -->
     <script>
             var link = document.createElement( 'link' );
             link.rel = 'stylesheet';
             link.type = 'text/css';
             link.href = window.location.search.match( /print-pdf/gi ) ? 'css/print/pdf.css' : 'css/print/paper.css';
             document.getElementsByTagName( 'head' )[0].appendChild( link );
     </script>
         <!--[if lt IE 9]>
         <script src="{reveal_path}lib/js/html5shiv.js"></script>
         <![endif]-->
    """.format(**meta)

        if False: self.header += """
    <!-- Loading the mathjax macro -->
    <!-- Load mathjax -->
    <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
    <!-- MathJax configuration -->
    <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
        //TeX: { equationNumbers: { autoNumber: "AMS" } },
         tex2jax: {
            inlineMath: [['$','$']],
            displayMath: [['$$','$$']],
            processEscapes: true,
            processEnvironments: true
        },
        // Center justify equations in code and markdown cells. Elsewhere
        // we use CSS to left justify single line equations in code cells.
        displayAlign: 'center',
        //"HTML-CSS": {
        //    styles: {'.MathJax_Display': {"margin": 0}},
        //    linebreaks: { automatic: true },
        //    availableFonts: ["TeX"]
        //    }
        //}
    });
    </script>
    <!-- End of mathjax configuration -->
    """
        self.header += """
    <!-- Get Font-awesome from cdn -->
    <!-- <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.css"> -->
</head>

<body>
    <div class="reveal">
        <div class="slides">
        """

        self.footer = """
        </div>
    </div>

    <script src="{reveal_path}lib/js/head.min.js"></script>
    <script src="{reveal_path}js/reveal.js"></script>

        """.format(**meta)
        self.footer +="""
	<script>

            // Full list of configuration options available at:
            // https://github.com/hakimel/reveal.js#configuration
            Reveal.initialize({

        """
        self.footer +="""
                // The "normal" size of the presentation, aspect ratio will be preserved
                // when the presentation is scaled to fit different resolutions. Can be
                // specified using percentage units.
                width: {width},
                height: {height},

                // Factor of the display size that should remain empty around the content
                margin: {margin},
        """.format(**meta)
        self.footer +="""
                // Display a presentation progress bar
                progress: true,
                slideNumber: 'c/t',

                // Push each slide change to the browser history
                //history: false,

                // Vertical centering of slides
                center: false,

                // Enables touch navigation on devices with touch input
                touch: true,

                // Bounds for smallest/largest possible scale to apply to content
                minScale: 0.2,
                maxScale: 2.5,

                // Display controls in the bottom right corner
                controls: false,

                // Enable keyboard shortcuts for navigation
                keyboard: true,

                // Enable the slide overview mode
                overview: true,

                // Loop the presentation
                //loop: false,

                // Change the presentation direction to be RTL
                //rtl: false,

                // Number of milliseconds between automatically proceeding to the
                // next slide, disabled when set to 0, this value can be overwritten
                // by using a data-autoslide attribute on your slides
                //autoSlide: 0,

                // Enable slide navigation via mouse wheel
                //mouseWheel: false,

                // Parallax background image
                //parallaxBackgroundImage: '/Users/laurentperrinet/cloud_nas/2015_RTC/2014-04-17_HDR/figures/p4100011.jpg', // e.g. "https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg"

                // Parallax background size
                //parallaxBackgroundSize: '3200px 2000px', // CSS syntax, e.g. "2100px 900px" - currently only pixels are supported (don't use % or auto)

                // This slide transition gives best results:
                transition: 'fade', // default/cube/page/concave/zoom/linear/fade/none

                // Transition speed
                transitionSpeed: 'slow', // default/fast/slow

                // Transition style for full page backgrounds
                backgroundTransition: 'none', // default/linear/none

			    // Turns fragments on and off globally
                fragments: true,

                // Theme
                theme: '{theme}', // available themes are in /css/theme

        """.format(**meta)
        if self.meta['draft']:
            self.footer +="""
                // Notes are only visible to the speaker inside of the speaker view. If you wish to share your notes with others you can initialize reveal.js with the showNotes config value set to true. Notes will appear along the bottom of the presentations.
                showNotes: 'true',
        """
        self.footer +="""
                math: {{
            		mathjax: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js',
                    config: 'TeX-AMS_HTML-full'  // See http://docs.mathjax.org/en/latest/config-files.html
                }},

                // Optional reveal.js plugins
                dependencies: [
                        {{ src: '{reveal_path}lib/js/classList.js', condition: function() {{ return !document.body.classList; }} }},
                        {{ src: '{reveal_path}plugin/markdown/marked.js', condition: function() {{ return !!document.querySelector( '[data-markdown]' ); }} }},
                        {{ src: '{reveal_path}plugin/markdown/markdown.js', condition: function() {{ return !!document.querySelector( '[data-markdown]' ); }} }},
                        {{ src: '{reveal_path}plugin/highlight/highlight.js', async: true, callback: function() {{ hljs.initHighlightingOnLoad(); }} }},
                        {{ src: '{reveal_path}plugin/zoom-js/zoom.js', async: true }},
                        {{ src: 'http://cdn.jsdelivr.net/reveal.js/3.0.0/plugin/notes/notes.js', async: true }},
                        {{ src: '{reveal_path}plugin/math/math.js', async: true }},
                        {{ src: '{reveal_path}plugin/mathsvg/math.js', async: true }},
        """.format(reveal_path=self.meta['reveal_path'])#.replace('file://', ''))
                        # {{ src: '{reveal_path}plugin/search/search.js', async: true }},

# http://cdn.jsdelivr.net/reveal.js/3.0.0/plugin/notes/notes.html
# https://cdn.jsdelivr.net/npm/reveal.js@3.6.0/plugin/notes/notes.js
# http://cdn.jsdelivr.net/reveal.js/3.0.0/plugin/notes/notes.js
#                         {{ src: '{reveal_path}plugin/notes/notes.js', async: true }},

#  .reveal section
# -  margin: 15px 0px;
# +  margin: 0px 0px;
#    background: rgba(255, 255, 255, 0.12);
# -  border: 4px solid #eee;
# -  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); }
# +  border: 0px solid #eee;
# +  /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); */
# +}

        self.footer +="""
                ]
        });
        </script>



    </body>
</html>
        """

        self.body = ''

    def open_section(self):
        self.body +=  "<section>"

    def hide_slide(self, **kwargs):
        """
        do nothing
        """
        pass

    def data_uri(self, fname):
        return base64.b64encode(open(fname, 'rb').read()).decode('utf-8').replace('\n', '')

    def embed_image(self, image_fname):
        """
        convert to bytes
        https://www.iandevlin.com/blog/2012/09/html5/html5-media-and-data-uri

        """
        return 'data:image/{ext};base64,{data_uri}'.format(ext=image_fname[-3:], data_uri=self.data_uri(image_fname))

    def content_imagelet(self, fname, height_px):
        data_src = self.embed_image(fname)
        return '<img class="plain" data-src="{data_src}"  height="{height}px" />'.format(data_src=data_src, height=height_px)

    def embed_video(self, video_fname):
        """
        convert to bytes
        """
        return 'data:video/{ext};base64,{data_uri}'.format(ext=video_fname[-3:], data_uri=self.data_uri(video_fname))

    def add_slide(self, hide=False, image_fname=None, video_fname=None, content='', notes='', md=False, embed=None):
        if hide: return 'Slide hidden'

        if not image_fname is None:
            if (embed is None and self.meta['embed']) or ((not embed is None ) and embed):
                image_fname = self.embed_image(image_fname)
            slide = '<section data-background="{image_fname}" data-background-size="{width}px"> '.format(image_fname=image_fname, width = self.meta['width'])
        elif not video_fname is None:
            if (embed is None and self.meta['embed']) or ((not embed is None ) and embed):
                video_fname = self.embed_video(video_fname)
            slide = '<section data-background-video="{}">'.format(video_fname)
        elif md:
            slide = """
<section data-markdown>
<script type="text/template">
        """
        else:
            slide = "<section>"

        slide += content

        if md:
            slide += """
</script>
            """

        if not notes=='':
            slide +="""
                <aside class="notes">
                 {}
                </aside>
                """.format(markdown.markdown(notes))

        slide += """
</section>
        """
        self.body += slide

    def add_slide_outline(self, i=None, title='Outline', notes=''):
        content = self.content_title(title)  + '\n<ol>\n'
        for i_, section in enumerate(self.meta['sections']):
            if i_ is i:
                content += """
                    <h3>
                    <li>
                    <p class="fragment highlight-red">
                    {}
                    </p>
                    </li>
                    </h3>
                    """.format(section)
            else:
                content += """
                    <h3>
                    <li>
                    {}
                    </li>
                    </h3>
                    """.format(section)
        content += """
                     </ol>
                    """
        self.add_slide(content=content, notes=notes)

    def add_slide_summary(self, list_of_points, title='Interim summary', fragment=False, notes=''):
        content = self.content_title(title) + """
            <ul>
            """

        if fragment :
            fragment_begin = '<p class="fragment">'
        else:
            fragment_begin = '<p>'
        fragment_end = '</p>'


        for point in list_of_points:
#                        <p class="fragment grow"><li> {} </li></p>
            content += """
            {}
            <li>
                        {}
            </li>
            {}
                        """.format(point, fragment_begin, fragment_end)
        content += """
                     </ul>
                    """
        self.add_slide(content=content, notes=notes)

    def content_title(self, title):
        if title is None:
            return ''
        else:
            return "<h3>{}</h3>".format(title)


    def content_figures(self, list_of_figures, transpose=False,
                        list_of_weights=None, title=None, height=None, width=None,
                        embed=None, fragment=False, url=None,
                        bgcolor="white", cell_bgcolor="white"):
        content =  self.content_title(title)

        if height is None:
            height = self.meta['height']
        content += """
            <div align="center">
            <table border=0px VALIGN="center" bgcolor={bgcolor} height={height} />
            """.format(bgcolor=bgcolor, height=height)

        n_fig = len(list_of_figures)
        if list_of_weights is None:#str(int() ) +"%"
            sizes = [1./n_fig] * n_fig #+"%" for _ in list_of_figures]
        else:
            total_weight = sum(list_of_weights)
            sizes = [weight/total_weight for weight in list_of_weights]#1./n_fig*
            # print(sizes)
        if not transpose: # one line many columns
            content += """
            <tr padding=0px style="vertical-align:middle" bgcolor={bgcolor}>
            """.format(bgcolor=bgcolor)

        for i_, (size, image_fname) in enumerate(zip(sizes, list_of_figures)):
            if width is None:
                width_str = " "
                width_ = int(size*self.meta['width'])#*height/self.meta['height']
                # print(width_)
            else:
                width_ = int(size*width)
                width_str = 'width="{width_}px"'.format(width_=width_)

            if (embed is None and self.meta['embed']) or ((not embed is None ) and embed):
                # data_uri = base64.b64encode(open(fname, 'rb').read()).decode('utf-8').replace('\n', '')
                # fname = 'data:image/{ext};base64,{data_uri}'.format(ext=fname[-3:], data_uri=data_uri)
                image_fname = self.embed_image(image_fname)

            if fragment and i_>0:
                fragment_begin = '<p class="fragment">'
            else:
                fragment_begin = '<p>'

            if not url is None:
                fragment_begin += '<a href="' + url[i_] + '">'
                fragment_end = '</a></p>'
            else:
                fragment_end = '</p>'

            if not transpose: # one line many columns
                content += """
                <td height={height} width="{width}" padding-top=0px padding-bottom=0px style="text-align:center; vertical-align:middle" bgcolor="{cell_bgcolor}" />
                {fragment_begin}
                    <img class="plain" data-src="{fname}"  height="{height}px" {width_str} />
                {fragment_end}
                </td>
                """.format(cell_bgcolor=cell_bgcolor, height=int(height),
                           width=width_, width_str=width_str, fname=image_fname,
                           fragment_begin=fragment_begin, fragment_end=fragment_end)
            else:
                content += """
                <tr style="vertical-align:middle" bgcolor="{cell_bgcolor}"  height="{height_}px">
                    <td width="100%" style="text-align:center; vertical-align:middle" bgcolor="{cell_bgcolor}" />
                    {fragment_begin}
                        <img class="plain" data-src="{fname}"  height="{height_}px"  />
                    {fragment_end}
                    </td>
                </tr>
                """.format(cell_bgcolor=cell_bgcolor, height_=int(size*height),
                        fname=image_fname,
                        fragment_begin=fragment_begin, fragment_end=fragment_end)

        # closing table
        if not transpose: # one line many columns
            content += """
            </tr>
            """
        content += """
        </table>
        </div>
        """
        return content
    def content_bib(self, author, year, journal, url=None):
        if not url is None:
            journal = '<a href="{url}">{journal}</a>'.format(journal=journal, url=url)
        return """
        <div style="text-align:right;">{author} ({year}) <em>{journal}</em>  </div>
        """.format(author=author, year=year, journal=journal)
        return content

    def close_section(self):
        self.body +=  "\n</section>\n"

    def compile(self, filename='index.html'):
        html = self.header + self.body + self.footer
        with open(filename, 'w') as f: f.write(html)
# s.body += """
# <script>
#       document.getElementById('theme').setAttribute('href','css/theme/white.css'); return false;">
# </script>
