from flask import redirect, url_for

def try_redirect(request, fallback, **kwargs):
    redirect_from = request.args.get("redir")
    redirect_from_id = request.args.get("redir_id")

    try:
        if redirect_from:
            if redirect_from_id:
                return redirect(url_for(redirect_from, **kwargs, id=redirect_from_id))
            else:
                return redirect(url_for(redirect_from, **kwargs))
    except:
        pass
    
    return redirect(url_for(fallback, **kwargs))