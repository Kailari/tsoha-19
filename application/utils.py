from flask import redirect, url_for


def try_redirect(fallback, **kwargs):
    redirect_target = kwargs.pop("redir", fallback)
    redirect_target_id = kwargs.pop("redir_id", None)

    try:
        if redirect_target_id:
            return redirect(url_for(redirect_target, id=redirect_target_id, **kwargs))
        else:
            return redirect(url_for(redirect_target, **kwargs))
    except:
        pass

    return redirect(url_for(fallback, **kwargs))
