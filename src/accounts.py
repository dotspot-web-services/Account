
from setApp import accounts
from profile.urls import profs
from registry.urls import accs
from user.urls import usrs
from geos.urls import geo


accounts.register_blueprint(accs, url_prefix="/accounts")
accounts.register_blueprint(profs, url_prefix="/profiles")
accounts.register_blueprint(usrs, url_prefix="/users")
accounts.register_blueprint(geo, url_prefix="/geoip")


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
    #print(accounts.url_map)
    accounts.run(port=5000, threaded=True)


def urlMap():
    """
    form_data["info"] = {"info": request.user_agent.string, "usr_ip": request.remote_addr}
    Map([<Rule '/profiles/api/Accademics' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> profa.accademics>,
    <Rule '/profiles/api/Researcher' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> profa.resacher>,
    <Rule '/profiles/app/accademics' (POST, OPTIONS) -> profs.prof.acadas>,
    <Rule '/profiles/app/academics' (HEAD, OPTIONS, GET) -> profs.prof.acadForm>,
    <Rule '/profiles/app/researchs' (HEAD, OPTIONS, GET) -> profs.prof.resrchForm>,
    <Rule '/profiles/app/researchs' (POST, OPTIONS) -> profs.prof.resrcha>,
    <Rule '/accounts/api/outreach' (HEAD, OPTIONS, GET, POST) -> rega.message>,
    <Rule '/accounts/app/finalize' (HEAD, OPTIONS, GET) -> accs.regs.finalPage>,
    <Rule '/accounts/app/finalize' (POST, OPTIONS) -> accs.regs.finalize>,
    <Rule '/accounts/app/register' (POST, OPTIONS) -> accs.regs.register>,
    <Rule '/accounts/app/register' (HEAD, OPTIONS, GET) -> accs.regs.regPage>,
    <Rule '/accounts/api/logout' (HEAD, OPTIONS, GET, POST) -> rega.logout>,
    <Rule '/accounts/app/signIn' (HEAD, OPTIONS, GET) -> accs.regs.signInPage>,
    <Rule '/accounts/app/signIn' (POST, OPTIONS) -> accs.regs.signIn>,
    <Rule '/accounts/app/logOut' (HEAD, OPTIONS, GET) -> accs.regs.confLogOut>,
    <Rule '/accounts/app/logOut' (POST, OPTIONS) -> accs.regs.logOut>,
    <Rule '/profiles/api/Basics' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> profa.basic>,
    <Rule '/profiles/app/basics' (HEAD, OPTIONS, GET) -> profs.prof.basicForm>,
    <Rule '/profiles/app/basics' (POST, OPTIONS) -> profs.prof.basics>,
    <Rule '/accounts/api/login' (HEAD, POST, GET, PUT, OPTIONS) -> rega.login>,
    <Rule '/accounts/app/reset' (HEAD, OPTIONS, GET) -> accs.regs.resetPage>,
    <Rule '/accounts/app/reset' (POST, OPTIONS) -> accs.regs.reset>,
    <Rule '/profiles/api/Works' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> profa.works>,
    <Rule '/profiles/app/works' (HEAD, OPTIONS, GET) -> profs.prof.workForm>,
    <Rule '/profiles/app/works' (POST, OPTIONS) -> profs.prof.works>,
    <Rule '/accounts/api/reg' (HEAD, POST, GET, PUT, OPTIONS) -> rega.register>,
    <Rule '/users/api/publications' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> groca.pubs>,
    <Rule '/users/api/pictures' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> groca.avatars>,
    <Rule '/users/api/profiles' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> groca.profiles>,
    <Rule '/users/api/socials' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> groca.socs>,
    <Rule '/users/app/profile' (HEAD, OPTIONS, GET) -> grocs.groc.prof>,
    <Rule '/users/api/awards' (HEAD, POST, GET, DELETE, PUT, OPTIONS) -> groca.awards>,
    <Rule '/users/app/social' (POST, OPTIONS) -> grocs.groc.cr8hub>,
    <Rule '/users/app/social' (HEAD, OPTIONS, GET) -> grocs.groc.hubs>,
    <Rule '/users/app/mindme' (POST, OPTIONS) -> grocs.groc.cr8minda>,
    <Rule '/users/app/mindme' (HEAD, OPTIONS, GET) -> grocs.groc.minda>,
    <Rule '/users/app/award' (POST, OPTIONS) -> grocs.groc.cr8award>,
    <Rule '/users/app/award' (HEAD, OPTIONS, GET) -> grocs.groc.awards>,
    <Rule '/users/app/pubs' (POST, OPTIONS) -> grocs.groc.cr8pub>,
    <Rule '/users/app/pubs' (HEAD, OPTIONS, GET) -> grocs.groc.pubs>,
    <Rule '/users/app/pix' (POST, OPTIONS) -> grocs.groc.cr8pix>,
    <Rule '/users/app/pix' (HEAD, OPTIONS, GET) -> grocs.groc.pixs>,
    <Rule '/geoip/signature' (HEAD, POST, OPTIONS, GET) -> geo.ipregistry>,
    <Rule '/geoip/places' (HEAD, POST, OPTIONS, GET) -> geo.geodata>,
    <Rule '/' (HEAD, OPTIONS, GET) -> index>,
    <Rule '/accounts/api/registry/<filename>' (HEAD, OPTIONS, GET) -> accs.rega.static>,
    <Rule '/profiles/profile/<filename>' (HEAD, OPTIONS, GET) -> profs.static>,
    <Rule '/geoip/geodata/<filename>' (HEAD, OPTIONS, GET) -> geo.static>,
    <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>])
    """
    postgres_pwd = "dsO3YZ1KschiF7KhDChQ"
    accuser = "6j5DduC0HTdrwB1G9qGo = accountsdb"
    arenz = "8fYQYPVDlmO8zQ7GpYBg = arenzdb"
    spoter = "8uuH0Q5lUmToSNIJZXzT = spotlightsdb"
    servs = "zIiq9yW152nKbZwdr81K = servicesdb"