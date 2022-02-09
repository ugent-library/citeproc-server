Name: citeproc-server
Summary: node.js based Citation Style Language service
License: bsd
Version: 0.1
Release: X
BuildArch: x86_64
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: nodejs,npm
Source: %{name}.tar.gz

%description

%prep
%setup -q -n %{name}

%build
echo "nothing to build"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/opt/%{name}
mkdir -p %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/var/log/%{name}

cp -r $RPM_BUILD_DIR/%{name}/* %{buildroot}/opt/%{name}/
cp $RPM_BUILD_DIR/%{name}/systemd/%{name}.service %{buildroot}/etc/systemd/system/

echo "Complete!"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/%{name}/
%attr(444, -, -) /etc/systemd/system/%{name}.service
%attr(744, %{name}, citeproc-server) /var/log/%{name}

%doc

%pre
getent group %{name} >/dev/null || groupadd %{name}
getent passwd %{name} >/dev/null || useradd -g %{name} -s /sbin/nologin -c "citeproc server user" %{name}

exit 0

%post
systemctl daemon-reload &&
systemctl enable citeproc-server &&
systemctl restart citeproc-server

exit 0

%preun
if [ "$1" = 0 ] ; then
  systemctl stop citeproc-server
  systemctl disable citeproc-server
fi

exit 0

%postun

%changelog
