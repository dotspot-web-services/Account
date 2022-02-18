
from setApp import accounts
from profile.urls import profs
from registry.urls import accs
from user.urls import usrs


accounts.register_blueprint(accs, url_prefix="/accounts")
accounts.register_blueprint(profs, url_prefix="/profiles")
accounts.register_blueprint(usrs, url_prefix="/users")


if __name__ == "__main__":
    import string
    import secrets
    alphabet = string.ascii_letters + string.digits
    while True: 
        password = "".join(secrets.choice(alphabet) for i in range(20)) 
        if (any(c.islower() for c in password) 
            and any(c.isupper() for c in password) 
            and sum(c.isdigit() for c in password) >= 3): 
            break
    accounts.run(debug=True, port=3000)


def urlMap():
    """
    form_data["info"] = {"info": request.user_agent.string, "usr_ip": request.remote_addr}
        Map([<Rule '/profiles/api/Accademics' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> profa.accademics>,
        <Rule '/profiles/api/Researcher' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> profa.resacher>,
        <Rule '/profiles/app/accademics' (OPTIONS, POST) -> profs.prof.acadas>,
        <Rule '/profiles/app/academics' (HEAD, GET, OPTIONS) -> profs.prof.acadForm>,
        <Rule '/profiles/app/researchs' (HEAD, GET, OPTIONS) -> profs.prof.resrchForm>,
        <Rule '/profiles/app/researchs' (OPTIONS, POST) -> profs.prof.resrcha>,
        <Rule '/accounts/app/finalize' (HEAD, GET, OPTIONS) -> accs.regs.finalPage>,
        <Rule '/accounts/app/finalize' (OPTIONS, POST) -> accs.regs.finalize>,
        <Rule '/accounts/app/register' (OPTIONS, POST) -> accs.regs.register>,
        <Rule '/accounts/app/register' (HEAD, GET, OPTIONS) -> accs.regs.regPage>,
        <Rule '/profiles/app/profile' (HEAD, GET, OPTIONS) -> profs.prof.profile>,
        <Rule '/accounts/api/logout' (HEAD, GET, OPTIONS, POST) -> rega.logout>,
        <Rule '/accounts/app/signIn' (HEAD, GET, OPTIONS) -> accs.regs.signInPage>,
        <Rule '/accounts/app/signIn' (OPTIONS, POST) -> accs.regs.signIn>,
        <Rule '/accounts/app/logOut' (HEAD, GET, OPTIONS) -> accs.regs.confLogOut>,
        <Rule '/accounts/app/logOut' (OPTIONS, POST) -> accs.regs.logOut>,
        <Rule '/profiles/api/Basics' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> profa.basic>,
        <Rule '/profiles/app/basics' (HEAD, GET, OPTIONS) -> profs.prof.basicForm>,
        <Rule '/profiles/app/basics' (OPTIONS, POST) -> profs.prof.basics>,
        <Rule '/accounts/api/login' (POST, PUT, HEAD, GET, OPTIONS) -> rega.login>,
        <Rule '/accounts/app/reset' (HEAD, GET, OPTIONS) -> accs.regs.resetPage>,
        <Rule '/accounts/app/reset' (OPTIONS, POST) -> accs.regs.reset>,
        <Rule '/profiles/api/Works' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> profa.works>,
        <Rule '/profiles/app/works' (HEAD, GET, OPTIONS) -> profs.prof.workForm>,
        <Rule '/profiles/app/works' (OPTIONS, POST) -> profs.prof.works>,
        <Rule '/accounts/api/reg' (POST, PUT, HEAD, GET, OPTIONS) -> rega.register>,
        <Rule '/users/api/publications' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> groca.pubs>,
        <Rule '/users/api/pictures' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> groca.avatars>,
        <Rule '/users/api/profiles' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> groca.profiles>,
        <Rule '/users/api/socials' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> groca.socs>,
        <Rule '/users/app/profile' (HEAD, GET, OPTIONS) -> grocs.groc.prof>,
        <Rule '/users/api/awards' (DELETE, POST, PUT, HEAD, GET, OPTIONS) -> groca.awards>,
        <Rule '/users/app/social' (OPTIONS, POST) -> grocs.groc.cr8hub>,
        <Rule '/users/app/social' (HEAD, GET, OPTIONS) -> grocs.groc.hubs>,
        <Rule '/users/app/mindme' (OPTIONS, POST) -> grocs.groc.cr8minda>,
        <Rule '/users/app/mindme' (HEAD, GET, OPTIONS) -> grocs.groc.minda>,
        <Rule '/users/app/award' (OPTIONS, POST) -> grocs.groc.cr8award>,
        <Rule '/users/app/award' (HEAD, GET, OPTIONS) -> grocs.groc.awards>,
        <Rule '/users/app/pubs' (OPTIONS, POST) -> grocs.groc.cr8pub>,
        <Rule '/users/app/pubs' (HEAD, GET, OPTIONS) -> grocs.groc.pubs>,
        <Rule '/users/app/pix' (OPTIONS, POST) -> grocs.groc.cr8pix>,
        <Rule '/users/app/pix' (HEAD, GET, OPTIONS) -> grocs.groc.pixs>,
        <Rule '/' (HEAD, GET, OPTIONS) -> index>,
        <Rule '/accounts/api/registry/<filename>' (HEAD, GET, OPTIONS) -> accs.rega.static>,
        <Rule '/profiles/profile/<filename>' (HEAD, GET, OPTIONS) -> profs.static>,
        <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>])
    """
    postgres_pwd = "dsO3YZ1KschiF7KhDChQ"
    accuser = "6j5DduC0HTdrwB1G9qGo = accountsdb"
    arenz = "8fYQYPVDlmO8zQ7GpYBg = arenzdb"
    spoter = "8uuH0Q5lUmToSNIJZXzT = spotlightsdb"
    servs = "zIiq9yW152nKbZwdr81K = servicesdb"