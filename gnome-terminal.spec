Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.1.3
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.1/%{name}-%{version}.tar.bz2
Patch0:		%{name}-TERM.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 1.2.1-10
BuildRequires:	Xft-devel >= 2.0-6
BuildRequires:	gtk+2-devel >= 2.1.3-3
BuildRequires:	libglade2-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.1.2
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	rpm-build >= 4.1-8.2
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.4
BuildRequires:	vte-devel >= 0.10.5
Requires:	libgnomeui >= 2.1.2
Requires(post,postun):	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl
To jest terminal, na razie ca³kowicie nie dokoñczony.

%prep
%setup -q 
%patch0 -p1

%build
%configure \
	--with-widget=vte
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post 
scrollkeeper-update
%gconf_schema_install

%postun
scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog NEWS TODO AUTHORS
%doc %{_omf_dest_dir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_libdir}/bonobo/servers/*
%{_datadir}/pixmaps/*
