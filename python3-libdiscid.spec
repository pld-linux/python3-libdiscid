#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Python bindings for libdiscid library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libdiscid
Name:		python3-libdiscid
Version:	2.0.3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/python-libdiscid
Source0:	https://files.pythonhosted.org/packages/source/p/python-libdiscid/python-libdiscid-%{version}.tar.gz
# Source0-md5:	f7ae90cfff90ffcb3332540e7a209997
URL:		https://github.com/sebastinas/python-libdiscid
BuildRequires:	libdiscid-devel
BuildRequires:	python3-Cython >= 0.15
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-installer
BuildRequires:	python3-pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for libdiscid library.

%description -l pl.UTF-8
Wiązania Pythona do biblioteki libdiscid.

%package apidocs
Summary:	API documentation for Python libdiscid module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona libdiscid
Group:		Documentation

%description apidocs
API documentation for Python libdiscid module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona libdiscid.

%prep
%setup -q -n python-libdiscid-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" build-3-test/libdiscid/tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH="$PWD/build-3-doc" \
sphinx-build -b html docs docs/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/libdiscid/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md CHANGELOG.md
%dir %{py3_sitedir}/libdiscid
%attr(755,root,root) %{py3_sitedir}/libdiscid/_discid.cpython-*.so
%{py3_sitedir}/libdiscid/*.py
%{py3_sitedir}/libdiscid/__pycache__
%{py3_sitedir}/libdiscid/_discid.pyi
%{py3_sitedir}/libdiscid/py.typed
%{py3_sitedir}/libdiscid/compat
%{py3_sitedir}/python_libdiscid-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/{_static,*.html,*.js}
%endif
