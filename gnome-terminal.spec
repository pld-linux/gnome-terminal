Summary:	-
Summary(pl):	-
Name:		gnome-terminal
Version:	1.9.6
Release:	0.1
License:	GPL
Group:		-
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	libzvt-devel >= 1.115.2
BuildRequires:	gtk+2-devel >= 2.0.2
BuildRequires:	GConf2-devel >= 1.1.10
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME2

%description

%description -l pl

%prep
%setup -q 

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README ChangeLog NEWS TODO AUTHORS

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post 
GCONF_CONFIG_SOURCE="" %{_bindir}/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_libdir}/bonobo/servers/*
%{_datadir}/pixmaps/*
#no doc
#%{_datadir}/gnome/help/%{name}
