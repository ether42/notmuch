%global git 6b9a717c
%global date %(date +%Y%m%d)

# If you are doing a git snapshot:
#
# Release should be 1%{git}%{?dist}
# Source0 should be notmuch-%{version}-%{git}.tar.gz
# git version is generated by 'git show-ref --hash=8 HEAD'
#
# To create a tarball:
#
# git clone git://notmuchmail.org/git/notmuch
# cd notmuch
# git archive --format=tar --prefix=notmuch-0.4/ HEAD | gzip > notmuch-0.4-`git show-ref --hash=8 HEAD`.tar.gz
#

Name:           notmuch
Version:        0.15.2
Release:        3%{?dist}
Summary:        Thread-based email index, search and tagging

Group:          Applications/Internet
License:        GPLv3+
URL:            https://notmuchmail.org/

Source0:        https://notmuchmail.org/releases/notmuch-%{version}.tar.gz

BuildRequires:  xapian-core-devel gmime-devel libtalloc-devel
BuildRequires:  zlib-devel emacs-el emacs-nox python ruby ruby-devel perl

%description
Fast system for indexing, searching, and tagging email.  Even if you
receive 12000 messages per month or have on the order of millions of
messages that you've been saving for decades, Notmuch will be able to
quickly search all of it.

Notmuch is not much of an email program. It doesn't receive messages
(no POP or IMAP support). It doesn't send messages (no mail composer,
no network code at all). And for what it does do (email search) that
work is provided by an external library, Xapian. So if Notmuch
provides no user interface and Xapian does all the heavy lifting, then
what's left here? Not much.

%package devel
Summary:        Development libraries and header files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n emacs-notmuch
Summary:        Not much support for Emacs
Group:          Applications/Editors
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}, emacs(bin) >= %{_emacs_version}

%description -n emacs-notmuch
%{summary}.

%package -n python-notmuch
Summary:        Python bindings for notmuch
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description -n python-notmuch
%{summary}.

%package -n notmuch-ruby
Summary:        Ruby bindings for notmuch
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description -n notmuch-ruby
%{summary}.

%package mutt
Summary:        Notmuch (of a) helper for Mutt
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       perl(Term::ReadLine::Gnu)

%description mutt
notmuch-mutt provide integration among the Mutt mail user agent and
the Notmuch mail indexer.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} --includedir=%{_includedir} --emacslispdir=%{_emacs_sitelispdir}
make %{?_smp_mflags} CFLAGS="%{optflags}"

pushd bindings/python
    python setup.py build
popd

pushd bindings/ruby
    export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
    ruby extconf.rb --vendor
    make
popd

pushd contrib/notmuch-mutt
    make
popd

%install
make install DESTDIR=%{buildroot}

pushd bindings/python
    python setup.py install -O1 --skip-build --root %{buildroot}
popd

pushd bindings/ruby
    make install DESTDIR=%{buildroot}
popd

install contrib/notmuch-mutt/notmuch-mutt %{buildroot}%{_bindir}/notmuch-mutt
install contrib/notmuch-mutt/notmuch-mutt.1 %{buildroot}%{_mandir}/man1/notmuch-mutt.1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING COPYING-GPL-3 INSTALL README
%{_sysconfdir}/bash_completion.d/notmuch
%{_datadir}/zsh/functions/Completion/Unix/_notmuch
%{_bindir}/notmuch
%{_mandir}/man?/*
%{_libdir}/libnotmuch.so.3*

%files devel
%{_libdir}/libnotmuch.so
%{_includedir}/*

%files -n emacs-notmuch
%{_emacs_sitelispdir}/*

%files -n python-notmuch
%doc bindings/python/README
%{python_sitelib}/*

%files -n notmuch-ruby
%{ruby_vendorarchdir}/*

%files mutt
%{_bindir}/notmuch-mutt
%{_mandir}/man1/notmuch-mutt.1*

%changelog
* Sun Apr 28 2013 Felipe Contreras <felipe.contreras@gmail.com> - 0.15.2-3
- Add ruby bingings

* Sun Apr 28 2013 Felipe Contreras <felipe.contreras@gmail.com> - 0.15.2-2
- Sync with Fedora

* Sun Apr 28 2013 Felipe Contreras <felipe.contreras@gmail.com> - 0.15.2-1
- Update to latest upstream

* Tue Nov  2 2010 Scott Henson <shenson@redhat.com> - 0.4-1
- New upstream release

* Wed Nov 18 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.3.306635c2
- First version

