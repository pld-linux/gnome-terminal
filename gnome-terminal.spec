# --with zvt	build with ZVT not VTE terminal widget
Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.1.2
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.1/%{name}-%{version}.tar.bz2
Patch0:		%{name}-TERM.patch
#Patch1:		%{name}-pango-zvt.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	gtk+2-devel >= 2.0.3
BuildRequires:	libglade2-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.1.2
%{?_with_zvt:BuildRequires:	libzvt-devel >= 2.0.0}
%{?!_with_zvt:BuildRequires:	vte-devel >= 0.10.4}
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	scrollkeeper
BuildRequires:	rpm-build >= 4.1-7
Requires:	libgnomeui >= 2.1.2
Requires(post,postun):	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME2
%define		_serverdir	/usr/lib/bonobo/servers

%description
This is a terminal thing that isn't finished at all.

%description -l pl
To jest terminal, na razie ca³kowicie nie dokoñczony.

%prep
%setup -q 
%patch0 -p1
#%patch1 -p1

%build
%configure \
	--with-widget=%{?!_with_zvt:vte}%{?_with_zvt:zvt}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 \
	serverdir=%{_serverdir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post 
scrollkeeper-update
GCONF_CONFIG_SOURCE="`%{_bindir}/gconftool-2 --get-default-source`" %{_bindir}/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null

%postun
scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog NEWS TODO AUTHORS
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_serverdir}/*
%{_datadir}/pixmaps/*
%doc %{_omf_dest_dir}/%{name}
