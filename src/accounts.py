
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
        Map([<Rule '/profiles/api/Accademics' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> profa.accademics>,
        <Rule '/profiles/api/Researcher' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> profa.resacher>,
        <Rule '/profiles/app/accademics' (OPTIONS, POST) -> profs.prof.acadas>,
        <Rule '/profiles/app/academics' (OPTIONS, HEAD, GET) -> profs.prof.acadForm>,
        <Rule '/profiles/app/researchs' (OPTIONS, HEAD, GET) -> profs.prof.resrchForm>,
        <Rule '/profiles/app/researchs' (OPTIONS, POST) -> profs.prof.resrcha>,
        <Rule '/accounts/app/finalize' (OPTIONS, HEAD, GET) -> accs.regs.finalPage>,
        <Rule '/accounts/app/finalize' (OPTIONS, POST) -> accs.regs.finalize>,
        <Rule '/accounts/app/register' (OPTIONS, POST) -> accs.regs.register>,
        <Rule '/accounts/app/register' (OPTIONS, HEAD, GET) -> accs.regs.regPage>,
        <Rule '/accounts/api/logout' (OPTIONS, HEAD, GET, POST) -> rega.logout>,
        <Rule '/accounts/app/signIn' (OPTIONS, HEAD, GET) -> accs.regs.signInPage>,
        <Rule '/accounts/app/signIn' (OPTIONS, POST) -> accs.regs.signIn>,
        <Rule '/accounts/app/logOut' (OPTIONS, HEAD, GET) -> accs.regs.confLogOut>,
        <Rule '/accounts/app/logOut' (OPTIONS, POST) -> accs.regs.logOut>,
        <Rule '/profiles/api/Basics' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> profa.basic>,
        <Rule '/profiles/app/basics' (OPTIONS, HEAD, GET) -> profs.prof.basicForm>,
        <Rule '/profiles/app/basics' (OPTIONS, POST) -> profs.prof.basics>,
        <Rule '/accounts/api/login' (GET, PUT, POST, OPTIONS, HEAD) -> rega.login>,
        <Rule '/accounts/app/reset' (OPTIONS, HEAD, GET) -> accs.regs.resetPage>,
        <Rule '/accounts/app/reset' (OPTIONS, POST) -> accs.regs.reset>,
        <Rule '/profiles/api/Works' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> profa.works>,
        <Rule '/profiles/app/works' (OPTIONS, HEAD, GET) -> profs.prof.workForm>,
        <Rule '/profiles/app/works' (OPTIONS, POST) -> profs.prof.works>,
        <Rule '/accounts/api/reg' (GET, PUT, POST, OPTIONS, HEAD) -> rega.register>,
        <Rule '/users/api/publications' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> groca.pubs>,
        <Rule '/users/api/pictures' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> groca.avatars>,
        <Rule '/users/api/profiles' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> groca.profiles>,
        <Rule '/users/api/socials' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> groca.socs>,
        <Rule '/users/app/profile' (OPTIONS, HEAD, GET) -> grocs.groc.prof>,
        <Rule '/users/app/profile' (OPTIONS, HEAD, GET) -> grocs.groc.profile>,
        <Rule '/users/api/awards' (GET, PUT, POST, OPTIONS, DELETE, HEAD) -> groca.awards>,
        <Rule '/users/app/social' (OPTIONS, POST) -> grocs.groc.cr8hub>,
        <Rule '/users/app/social' (OPTIONS, HEAD, GET) -> grocs.groc.hubs>,
        <Rule '/users/app/mindme' (OPTIONS, POST) -> grocs.groc.cr8minda>,
        <Rule '/users/app/mindme' (OPTIONS, HEAD, GET) -> grocs.groc.minda>,
        <Rule '/users/app/award' (OPTIONS, POST) -> grocs.groc.cr8award>,
        <Rule '/users/app/award' (OPTIONS, HEAD, GET) -> grocs.groc.awards>,
        <Rule '/users/app/pubs' (OPTIONS, POST) -> grocs.groc.cr8pub>,
        <Rule '/users/app/pubs' (OPTIONS, HEAD, GET) -> grocs.groc.pubs>,
        <Rule '/users/app/pix' (OPTIONS, POST) -> grocs.groc.cr8pix>,
        <Rule '/users/app/pix' (OPTIONS, HEAD, GET) -> grocs.groc.pixs>,
        <Rule '/' (OPTIONS, HEAD, GET) -> index>,
        <Rule '/accounts/api/registry/<filename>' (OPTIONS, HEAD, GET) -> accs.rega.static>,
        <Rule '/profiles/profile/<filename>' (OPTIONS, HEAD, GET) -> profs.static>,
        <Rule '/static/<filename>' (OPTIONS, HEAD, GET) -> static>])
    """
    postgres_pwd = "dsO3YZ1KschiF7KhDChQ"
    accuser = "6j5DduC0HTdrwB1G9qGo = accountsdb"
    arenz = "8fYQYPVDlmO8zQ7GpYBg = arenzdb"
    spoter = "8uuH0Q5lUmToSNIJZXzT = spotlightsdb"
    servs = "zIiq9yW152nKbZwdr81K = servicesdb"