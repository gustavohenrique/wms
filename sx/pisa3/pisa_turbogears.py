# -*- coding: ISO-8859-1 -*-
#############################################
## (C)opyright by Dirk Holtwick, 2002-2007 ##
## All rights reserved                     ##
#############################################

__reversion__ = "$Revision: 20 $"
__author__    = "$Author: holtwick $"
__date__      = "$Date: 2007-10-09 12:58:24 +0200 (Di, 09 Okt 2007) $"

from turbogears.decorator import weak_signature_decorator
import sx.pisa3 as pisa
import StringIO
import cherrypy

def to_pdf(filename=None, content_type="application/pdf"):
    def entangle(func):
        def decorated(func, *args, **kw):
            output = func(*args, **kw)
            dst = StringIO.StringIO()
            result = pisa.CreatePDF(
                StringIO.StringIO(output),
                dst
                )
            if not result.err:
                cherrypy.response.headers["Content-Type"] = content_type
                if filename:
                    cherrypy.response.headers["Content-Disposition"] = "attachment; filename=" + filename
                output = dst.getvalue()
            return output
        return decorated
    return weak_signature_decorator(entangle)

topdf = to_pdf
