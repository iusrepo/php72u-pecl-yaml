%global pecl_name yaml
%global ini_name  40-%{pecl_name}.ini

Name:           php-pecl-yaml
Version:        2.0.0
Release:        1%{?dist}
Summary:        Support for YAML 1.1 serialization using the LibYAML library
Group:          Development/Languages

License:        MIT
URL:            http://pecl.php.net/package/yaml
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRequires:  php-devel >= 7
BuildRequires:  php-pear
BuildRequires:  libyaml-devel

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}


%description
The YAML PHP Extension provides a wrapper to the LibYAML library. It gives the
user the ability to parse YAML document streams into PHP constructs and emit PHP
constructs as valid YAML 1.1 documents.

%prep
%setup -q -c

# Remove test file to avoid regsitration (pecl list-files yaml)
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    package.xml >%{pecl_name}-%{version}%{?prever}/package.xml


%build
cd %{pecl_name}-%{version}%{?prever}
phpize
%configure
make %{?_smp_mflags}


%check
cd %{pecl_name}-%{version}%{?prever}
make test NO_INTERACTION=1 REPORT_EXIT_STATUS=1


%install
cd %{pecl_name}-%{version}%{?prever}
make install INSTALL_ROOT=%{buildroot}

# Basic configuration
mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; %{pecl_name} extension configuration
; see http://www.php.net/manual/en/yaml.configuration.php

; Decode entities which have the explicit tag "tag:yaml.org,2002:binary"
yaml.decode_binary = 0
; Controls the decoding of "tag:yaml.org,2002:timestamp"
; 0 will not apply any decoding.
; 1 will use strtotime().
; 2 will use date_create().
yaml.decode_timestamp = 0
; Cause canonical form output.
yaml.output_canonical = 0
; Number of spaces to indent sections. Value should be between 1 and 10.
yaml.output_indent = 2
; Set the preferred line width. -1 means unlimited.
yaml.output_width = 80
; Enable/disable serialized php object processing.
yaml.decode_php = 0
EOF

# Package info
mkdir -p %{buildroot}%{pecl_xmldir}
install -p -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%files
%license %{pecl_name}-%{version}%{?prever}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{_sysconfdir}/php.d/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- upate to 2.0.0
- fix project URL

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.RC8
- upate to 2.0.0RC8
- rebuild for https://fedoraproject.org/wiki/Changes/php70
- fix license installation

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- enable test suite for Koschei
- drop 1 known to fail test

* Tue Mar 08 2016 Theodore Lee <theo148@gmail.com> - 1.2.0-1
- Update to upstream 1.2.0 release
- Disable test suite until datetime handling is fixed

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-5
- provides php-yaml
- install doc in pecl_docdir
- cleanup

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.1-3
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Theodore Lee <theo148@gmail.com> - 1.1.1-1
- Update to upstream 1.1.1 release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.1.0-4
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Theodore Lee <theo148@gmail.com> - 1.1.0-1
- Update to upstream 1.1.0 release
- Drop upstreamed cflags patch

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-6
- build against php 5.4
- fix filters

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-4
- Fix commenting in module configuration

* Thu May 12 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-3
- Remove unused php_apiver macro
- Specify version in php-devel requires
- Note upstream report for CFLAGS patch
- Add check section
- Document options in default config file

* Wed May 04 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-2
- Update patch to preserve original compiler flags

* Tue May 03 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-1
- Initial package
