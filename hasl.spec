#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Hassle free SASL client library
Summary(pl.UTF-8):	Bezproblemowa biblioteka klienta SASL
Name:		hasl
Version:	0.4.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/pidgin/%{name}-%{version}.tar.xz
# Source0-md5:	74d7ac0cb88a5ca2e084776bff4057c0
URL:		https://keep.imfreedom.org/hasl/hasl/
# C17
BuildRequires:	gcc >= 6:7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.76
BuildRequires:	libidn-devel >= 1.38
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.76
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Hassle-free Authentication and Security Layer client library.

%description -l pl.UTF-8
HASL (Hassle-free Authentication and Security Layer) to bezproblemowa
biblioteka kliencka uwierzytlniania i bezpieczeństwa.

%package devel
Summary:	Header files for hasl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki hasl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.76
Requires:	libidn-devel >= 1.38

%description devel
Header files for hasl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hasl.

%package static
Summary:	Static hasl library
Summary(pl.UTF-8):	Statyczna biblioteka hasl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hasl library.

%description static -l pl.UTF-8
Statyczna biblioteka hasl.

%package apidocs
Summary:	API documentation for hasl library
Summary(pl.UTF-8):	Dokumentacja API biblioteki hasl
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for hasl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki hasl.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Ddocs=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/hasl $RPM_BUILD_ROOT%{_gidocdir}

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{pt_PT,pt}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_libdir}/libhasl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhasl.so.0
%{_libdir}/girepository-1.0/Hasl-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhasl.so
%{_includedir}/hasl-1.0
%{_datadir}/gir-1.0/Hasl-1.0.gir
%{_pkgconfigdir}/hasl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhasl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/hasl
%endif
