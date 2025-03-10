#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python 2 bindings for libdiscid library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libdiscid
Name:		python-libdiscid
Version:	1.0
Release:	10
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/python-libdiscid
Source0:	https://files.pythonhosted.org/packages/source/p/python-libdiscid/%{name}-%{version}.tar.gz
# Source0-md5:	073812900a274a5d41fd4afa4e0b61bf
URL:		https://github.com/sebastinas/python-libdiscid
BuildRequires:	libdiscid-devel
%if %{with python2}
BuildRequires:	python-Cython >= 0.15
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-pkgconfig
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.15
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-pkgconfig
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 bindings for libdiscid library.

%description -l pl.UTF-8
Wiązania Pythona 2 do biblioteki libdiscid.

%package -n python3-libdiscid
Summary:	Python 3 bindings for libdiscid library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libdiscid
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-libdiscid
Python 3 bindings for libdiscid library.

%description -n python3-libdiscid -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libdiscid.

%package apidocs
Summary:	API documentation for Python libdiscid module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona libdiscid
Group:		Documentation

%description apidocs
API documentation for Python libdiscid module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona libdiscid.

%prep
%setup -q

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build -b html docs docs/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/libdiscid/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/libdiscid/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst changelog
%dir %{py_sitedir}/libdiscid
%attr(755,root,root) %{py_sitedir}/libdiscid/_discid.so
%{py_sitedir}/libdiscid/*.py[co]
%{py_sitedir}/libdiscid/compat
%{py_sitedir}/python_libdiscid-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-libdiscid
%defattr(644,root,root,755)
%doc LICENSE README.rst changelog
%dir %{py3_sitedir}/libdiscid
%attr(755,root,root) %{py3_sitedir}/libdiscid/_discid.cpython-*.so
%{py3_sitedir}/libdiscid/*.py
%{py3_sitedir}/libdiscid/__pycache__
%{py3_sitedir}/libdiscid/compat
%{py3_sitedir}/python_libdiscid-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/{_static,*.html,*.js}
%endif
