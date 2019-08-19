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
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/var/log/%{name}

cp -r $RPM_BUILD_DIR/%{name}/* %{buildroot}/opt/%{name}/
cp $RPM_BUILD_DIR/%{name}/init.d/%{name} %{buildroot}/etc/init.d/%{name}

echo "Complete!"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/%{name}/
%attr(755, -, -) /etc/init.d/%{name}
%attr(744, %{name}, citeproc-server) /var/log/%{name}

%doc

%pre
getent group %{name} >/dev/null || groupadd %{name}
getent passwd %{name} >/dev/null || useradd -g %{name} -s /sbin/nologin -c "citeproc server user" %{name}

#in case of an upgrade (first installs new version, then deletes old version)
has_service=$(chkconfig --list | grep %{name})
if [ "$has_service" != "" ];then
  chkconfig --del %{name} &> /dev/null
fi

exit 0

%post
(
cd /opt/%name &&
chkconfig --add %{name} && chkconfig --level 345 %{name} on &&
echo "service %{name} installed!"
) || exit 1

%preun
if [ "$1" = 0 ] ; then
  chkconfig --del %{name} &> /dev/null
  /usr/sbin/userdel -r %{name} &> /dev/null
  echo "service %{name} removed"
fi
exit 0

%postun

%changelog
