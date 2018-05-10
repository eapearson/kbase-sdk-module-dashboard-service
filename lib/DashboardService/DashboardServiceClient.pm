package DashboardService::DashboardServiceClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

DashboardService::DashboardServiceClient

=head1 DESCRIPTION


A KBase module: DashboardService


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => DashboardService::DashboardServiceClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 list_all_narratives

  $result, $stats = $obj->list_all_narratives($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DashboardService.ListAllNarrativesParams
$result is a DashboardService.ListAllNarrativesResult
$stats is a DashboardService.RunStats
ListAllNarrativesParams is a reference to a hash where the following keys are defined
ListAllNarrativesResult is a reference to a hash where the following keys are defined:
	narratives has a value which is a reference to a list where each element is a DashboardService.NarrativeX
	profiles has a value which is a reference to a list where each element is a DashboardService.UserProfile
NarrativeX is a reference to a hash where the following keys are defined:
	ws has a value which is a DashboardService.workspace_info
	nar has a value which is a DashboardService.object_info
	permissions has a value which is a reference to a list where each element is a DashboardService.UserPermission
workspace_info is a reference to a list containing 9 items:
	0: (id) an int
	1: (workspace) a string
	2: (owner) a string
	3: (moddate) a string
	4: (max_objid) an int
	5: (user_permission) a string
	6: (globalread) a string
	7: (lockstat) a string
	8: (metadata) a reference to a hash where the key is a string and the value is a string
object_info is a reference to a list containing 11 items:
	0: (objid) an int
	1: (name) a string
	2: (type) a string
	3: (save_date) a DashboardService.timestamp
	4: (version) an int
	5: (saved_by) a string
	6: (wsid) an int
	7: (workspace) a string
	8: (chsum) a string
	9: (size) an int
	10: (meta) a reference to a hash where the key is a string and the value is a string
timestamp is a string
UserPermission is a reference to a hash where the following keys are defined:
	username has a value which is a string
	permission has a value which is a DashboardService.permission
permission is a string
UserProfile is an UnspecifiedObject, which can hold any non-null object
RunStats is a reference to a hash where the following keys are defined:
	timings has a value which is a reference to a list where each element is a reference to a list containing 2 items:
		0: a string
		1: an int


</pre>

=end html

=begin text

$params is a DashboardService.ListAllNarrativesParams
$result is a DashboardService.ListAllNarrativesResult
$stats is a DashboardService.RunStats
ListAllNarrativesParams is a reference to a hash where the following keys are defined
ListAllNarrativesResult is a reference to a hash where the following keys are defined:
	narratives has a value which is a reference to a list where each element is a DashboardService.NarrativeX
	profiles has a value which is a reference to a list where each element is a DashboardService.UserProfile
NarrativeX is a reference to a hash where the following keys are defined:
	ws has a value which is a DashboardService.workspace_info
	nar has a value which is a DashboardService.object_info
	permissions has a value which is a reference to a list where each element is a DashboardService.UserPermission
workspace_info is a reference to a list containing 9 items:
	0: (id) an int
	1: (workspace) a string
	2: (owner) a string
	3: (moddate) a string
	4: (max_objid) an int
	5: (user_permission) a string
	6: (globalread) a string
	7: (lockstat) a string
	8: (metadata) a reference to a hash where the key is a string and the value is a string
object_info is a reference to a list containing 11 items:
	0: (objid) an int
	1: (name) a string
	2: (type) a string
	3: (save_date) a DashboardService.timestamp
	4: (version) an int
	5: (saved_by) a string
	6: (wsid) an int
	7: (workspace) a string
	8: (chsum) a string
	9: (size) an int
	10: (meta) a reference to a hash where the key is a string and the value is a string
timestamp is a string
UserPermission is a reference to a hash where the following keys are defined:
	username has a value which is a string
	permission has a value which is a DashboardService.permission
permission is a string
UserProfile is an UnspecifiedObject, which can hold any non-null object
RunStats is a reference to a hash where the following keys are defined:
	timings has a value which is a reference to a list where each element is a reference to a list containing 2 items:
		0: a string
		1: an int



=end text

=item Description



=back

=cut

 sub list_all_narratives
{
    my($self, @args) = @_;

# Authentication: optional

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function list_all_narratives (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to list_all_narratives:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'list_all_narratives');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DashboardService.list_all_narratives",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'list_all_narratives',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method list_all_narratives",
					    status_line => $self->{client}->status_line,
					    method_name => 'list_all_narratives',
				       );
    }
}
 


=head2 delete_narrative

  $obj->delete_narrative($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DashboardService.DeleteNarrativeParams
DeleteNarrativeParams is a reference to a hash where the following keys are defined:
	obji has a value which is a DashboardService.ObjectIdentity
ObjectIdentity is a reference to a hash where the following keys are defined:
	workspace_id has a value which is a DashboardService.ws_id
	object_id has a value which is a DashboardService.obj_id
	version has a value which is a DashboardService.obj_ver
ws_id is an int
obj_id is an int
obj_ver is an int

</pre>

=end html

=begin text

$params is a DashboardService.DeleteNarrativeParams
DeleteNarrativeParams is a reference to a hash where the following keys are defined:
	obji has a value which is a DashboardService.ObjectIdentity
ObjectIdentity is a reference to a hash where the following keys are defined:
	workspace_id has a value which is a DashboardService.ws_id
	object_id has a value which is a DashboardService.obj_id
	version has a value which is a DashboardService.obj_ver
ws_id is an int
obj_id is an int
obj_ver is an int


=end text

=item Description



=back

=cut

 sub delete_narrative
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function delete_narrative (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to delete_narrative:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'delete_narrative');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DashboardService.delete_narrative",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'delete_narrative',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method delete_narrative",
					    status_line => $self->{client}->status_line,
					    method_name => 'delete_narrative',
				       );
    }
}
 


=head2 share_narrative

  $obj->share_narrative($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DashboardService.ShareNarrativeParams
ShareNarrativeParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
	users has a value which is a reference to a list where each element is a DashboardService.username
	permission has a value which is a DashboardService.permission
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int
username is a string
permission is a string

</pre>

=end html

=begin text

$params is a DashboardService.ShareNarrativeParams
ShareNarrativeParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
	users has a value which is a reference to a list where each element is a DashboardService.username
	permission has a value which is a DashboardService.permission
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int
username is a string
permission is a string


=end text

=item Description



=back

=cut

 sub share_narrative
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function share_narrative (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to share_narrative:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'share_narrative');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DashboardService.share_narrative",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'share_narrative',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method share_narrative",
					    status_line => $self->{client}->status_line,
					    method_name => 'share_narrative',
				       );
    }
}
 


=head2 unshare_narrative

  $obj->unshare_narrative($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DashboardService.UnshareNarrativeParams
UnshareNarrativeParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
	users has a value which is a reference to a list where each element is a DashboardService.username
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int
username is a string

</pre>

=end html

=begin text

$params is a DashboardService.UnshareNarrativeParams
UnshareNarrativeParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
	users has a value which is a reference to a list where each element is a DashboardService.username
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int
username is a string


=end text

=item Description



=back

=cut

 sub unshare_narrative
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function unshare_narrative (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to unshare_narrative:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'unshare_narrative');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DashboardService.unshare_narrative",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'unshare_narrative',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method unshare_narrative",
					    status_line => $self->{client}->status_line,
					    method_name => 'unshare_narrative',
				       );
    }
}
 


=head2 share_narrative_global

  $obj->share_narrative_global($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DashboardService.ShareNarrativeGlobalParams
ShareNarrativeGlobalParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int

</pre>

=end html

=begin text

$params is a DashboardService.ShareNarrativeGlobalParams
ShareNarrativeGlobalParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int


=end text

=item Description



=back

=cut

 sub share_narrative_global
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function share_narrative_global (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to share_narrative_global:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'share_narrative_global');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DashboardService.share_narrative_global",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'share_narrative_global',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method share_narrative_global",
					    status_line => $self->{client}->status_line,
					    method_name => 'share_narrative_global',
				       );
    }
}
 


=head2 unshare_narrative_global

  $obj->unshare_narrative_global($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DashboardService.UnshareNarrativeGlobalParams
UnshareNarrativeGlobalParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int

</pre>

=end html

=begin text

$params is a DashboardService.UnshareNarrativeGlobalParams
UnshareNarrativeGlobalParams is a reference to a hash where the following keys are defined:
	wsi has a value which is a DashboardService.WorkspaceIdentity
WorkspaceIdentity is a reference to a hash where the following keys are defined:
	workspace has a value which is a DashboardService.ws_name
	id has a value which is a DashboardService.ws_id
ws_name is a string
ws_id is an int


=end text

=item Description



=back

=cut

 sub unshare_narrative_global
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function unshare_narrative_global (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to unshare_narrative_global:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'unshare_narrative_global');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DashboardService.unshare_narrative_global",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'unshare_narrative_global',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method unshare_narrative_global",
					    status_line => $self->{client}->status_line,
					    method_name => 'unshare_narrative_global',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "DashboardService.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "DashboardService.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'unshare_narrative_global',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method unshare_narrative_global",
            status_line => $self->{client}->status_line,
            method_name => 'unshare_narrative_global',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for DashboardService::DashboardServiceClient\n";
    }
    if ($sMajor == 0) {
        warn "DashboardService::DashboardServiceClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

@range [0,1]


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 timestamp

=over 4



=item Description

A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
character Z (representing the UTC timezone) or the difference
in time to UTC in the format +/-HHMM, eg:
    2012-12-17T23:24:06-0500 (EST time)
    2013-04-03T08:56:32+0000 (UTC time)
    2013-04-03T08:56:32Z (UTC time)


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 permission

=over 4



=item Description

Represents the permissions a user or users have to a workspace:

        'a' - administrator. All operations allowed.
        'w' - read/write.
        'r' - read.
        'n' - no permissions.


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 lock_status

=over 4



=item Description

The lock status of a workspace.
One of 'unlocked', 'locked', or 'published'.


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_id

=over 4



=item Description

from workspace_deluxe 
Note too that naming conventions for parameters using these types 
(may) also use the workspace_deluxe conventions.
workspace


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 obj_id

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 obj_ver

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 ws_name

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 WorkspaceIdentity

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace has a value which is a DashboardService.ws_name
id has a value which is a DashboardService.ws_id

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace has a value which is a DashboardService.ws_name
id has a value which is a DashboardService.ws_id


=end text

=back



=head2 ObjectIdentity

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_id has a value which is a DashboardService.ws_id
object_id has a value which is a DashboardService.obj_id
version has a value which is a DashboardService.obj_ver

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_id has a value which is a DashboardService.ws_id
object_id has a value which is a DashboardService.obj_id
version has a value which is a DashboardService.obj_ver


=end text

=back



=head2 username

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 object_info

=over 4



=item Description

Information about an object, including user provided metadata.

        obj_id objid - the numerical id of the object.
        obj_name name - the name of the object.
        type_string type - the type of the object.
        timestamp save_date - the save date of the object.
        obj_ver ver - the version of the object.
        username saved_by - the user that saved or copied the object.
        ws_id wsid - the workspace containing the object.
        ws_name workspace - the workspace containing the object.
        string chsum - the md5 checksum of the object.
        int size - the size of the object in bytes.
        usermeta meta - arbitrary user-supplied metadata about
            the object.


=item Definition

=begin html

<pre>
a reference to a list containing 11 items:
0: (objid) an int
1: (name) a string
2: (type) a string
3: (save_date) a DashboardService.timestamp
4: (version) an int
5: (saved_by) a string
6: (wsid) an int
7: (workspace) a string
8: (chsum) a string
9: (size) an int
10: (meta) a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a list containing 11 items:
0: (objid) an int
1: (name) a string
2: (type) a string
3: (save_date) a DashboardService.timestamp
4: (version) an int
5: (saved_by) a string
6: (wsid) an int
7: (workspace) a string
8: (chsum) a string
9: (size) an int
10: (meta) a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 workspace_info

=over 4



=item Description

Information about a workspace.

        ws_id id - the numerical ID of the workspace.
        ws_name workspace - name of the workspace.
        username owner - name of the user who owns (e.g. created) this workspace.
        timestamp moddate - date when the workspace was last modified.
        int max_objid - the maximum object ID appearing in this workspace.
            Since cloning a workspace preserves object IDs, this number may be
            greater than the number of objects in a newly cloned workspace.
        permission user_permission - permissions for the authenticated user of
            this workspace.
        permission globalread - whether this workspace is globally readable.
        lock_status lockstat - the status of the workspace lock.
        usermeta metadata - arbitrary user-supplied metadata about
            the workspace.


=item Definition

=begin html

<pre>
a reference to a list containing 9 items:
0: (id) an int
1: (workspace) a string
2: (owner) a string
3: (moddate) a string
4: (max_objid) an int
5: (user_permission) a string
6: (globalread) a string
7: (lockstat) a string
8: (metadata) a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a list containing 9 items:
0: (id) an int
1: (workspace) a string
2: (owner) a string
3: (moddate) a string
4: (max_objid) an int
5: (user_permission) a string
6: (globalread) a string
7: (lockstat) a string
8: (metadata) a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 SetItems

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
set_items_info has a value which is a reference to a list where each element is a DashboardService.object_info

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
set_items_info has a value which is a reference to a list where each element is a DashboardService.object_info


=end text

=back



=head2 ObjectInfo

=over 4



=item Description

Restructured workspace object info 'data' tuple:
id: data[0],
name: data[1],
type: data[2],
save_date: data[3],
version: data[4],
saved_by: data[5],
wsid: data[6],
ws: data[7],
checksum: data[8],
size: data[9],
metadata: data[10],
ref: data[6] + '/' + data[0] + '/' + data[4],
obj_id: 'ws.' + data[6] + '.obj.' + data[0],
typeModule: type[0],
typeName: type[1],
typeMajorVersion: type[2],
typeMinorVersion: type[3],
saveDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(data[3])


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is an int
name has a value which is a string
type has a value which is a string
save_date has a value which is a string
version has a value which is an int
saved_by has a value which is a string
wsid has a value which is an int
ws has a value which is a string
checksum has a value which is a string
size has a value which is an int
metadata has a value which is a reference to a hash where the key is a string and the value is a string
ref has a value which is a string
obj_id has a value which is a string
typeModule has a value which is a string
typeName has a value which is a string
typeMajorVersion has a value which is a string
typeMinorVersion has a value which is a string
saveDateMs has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is an int
name has a value which is a string
type has a value which is a string
save_date has a value which is a string
version has a value which is an int
saved_by has a value which is a string
wsid has a value which is an int
ws has a value which is a string
checksum has a value which is a string
size has a value which is an int
metadata has a value which is a reference to a hash where the key is a string and the value is a string
ref has a value which is a string
obj_id has a value which is a string
typeModule has a value which is a string
typeName has a value which is a string
typeMajorVersion has a value which is a string
typeMinorVersion has a value which is a string
saveDateMs has a value which is an int


=end text

=back



=head2 WorkspaceInfo

=over 4



=item Description

Restructured workspace info 'wsInfo' tuple:
id: wsInfo[0],
name: wsInfo[1],
owner: wsInfo[2],
moddate: wsInfo[3],
object_count: wsInfo[4],
user_permission: wsInfo[5],
globalread: wsInfo[6],
lockstat: wsInfo[7],
metadata: wsInfo[8],
modDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(wsInfo[3])


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is an int
name has a value which is a string
owner has a value which is a string
moddate has a value which is a DashboardService.timestamp
object_count has a value which is an int
user_permission has a value which is a DashboardService.permission
globalread has a value which is a DashboardService.permission
lockstat has a value which is a DashboardService.lock_status
metadata has a value which is a reference to a hash where the key is a string and the value is a string
modDateMs has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is an int
name has a value which is a string
owner has a value which is a string
moddate has a value which is a DashboardService.timestamp
object_count has a value which is an int
user_permission has a value which is a DashboardService.permission
globalread has a value which is a DashboardService.permission
lockstat has a value which is a DashboardService.lock_status
metadata has a value which is a reference to a hash where the key is a string and the value is a string
modDateMs has a value which is an int


=end text

=back



=head2 AppParam

=over 4



=item Definition

=begin html

<pre>
a reference to a list containing 3 items:
0: (step_pos) an int
1: (key) a string
2: (value) a string

</pre>

=end html

=begin text

a reference to a list containing 3 items:
0: (step_pos) an int
1: (key) a string
2: (value) a string


=end text

=back



=head2 Narrative

=over 4



=item Description

Listing Narratives / Naratorials (plus Narratorial Management)


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws has a value which is a DashboardService.workspace_info
nar has a value which is a DashboardService.object_info

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws has a value which is a DashboardService.workspace_info
nar has a value which is a DashboardService.object_info


=end text

=back



=head2 NarrativeList

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
narratives has a value which is a reference to a list where each element is a DashboardService.Narrative

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
narratives has a value which is a reference to a list where each element is a DashboardService.Narrative


=end text

=back



=head2 UserProfile

=over 4



=item Description

LIST ALL NARRATIVES


=item Definition

=begin html

<pre>
an UnspecifiedObject, which can hold any non-null object
</pre>

=end html

=begin text

an UnspecifiedObject, which can hold any non-null object

=end text

=back



=head2 UserPermission

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
username has a value which is a string
permission has a value which is a DashboardService.permission

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
username has a value which is a string
permission has a value which is a DashboardService.permission


=end text

=back



=head2 NarrativeX

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws has a value which is a DashboardService.workspace_info
nar has a value which is a DashboardService.object_info
permissions has a value which is a reference to a list where each element is a DashboardService.UserPermission

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws has a value which is a DashboardService.workspace_info
nar has a value which is a DashboardService.object_info
permissions has a value which is a reference to a list where each element is a DashboardService.UserPermission


=end text

=back



=head2 ListAllNarrativesResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
narratives has a value which is a reference to a list where each element is a DashboardService.NarrativeX
profiles has a value which is a reference to a list where each element is a DashboardService.UserProfile

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
narratives has a value which is a reference to a list where each element is a DashboardService.NarrativeX
profiles has a value which is a reference to a list where each element is a DashboardService.UserProfile


=end text

=back



=head2 ListAllNarrativesParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined
</pre>

=end html

=begin text

a reference to a hash where the following keys are defined

=end text

=back



=head2 RunStats

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
timings has a value which is a reference to a list where each element is a reference to a list containing 2 items:
	0: a string
	1: an int


</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
timings has a value which is a reference to a list where each element is a reference to a list containing 2 items:
	0: a string
	1: an int



=end text

=back



=head2 DeleteNarrativeParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obji has a value which is a DashboardService.ObjectIdentity

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obji has a value which is a DashboardService.ObjectIdentity


=end text

=back



=head2 ShareNarrativeParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity
users has a value which is a reference to a list where each element is a DashboardService.username
permission has a value which is a DashboardService.permission

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity
users has a value which is a reference to a list where each element is a DashboardService.username
permission has a value which is a DashboardService.permission


=end text

=back



=head2 UnshareNarrativeParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity
users has a value which is a reference to a list where each element is a DashboardService.username

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity
users has a value which is a reference to a list where each element is a DashboardService.username


=end text

=back



=head2 ShareNarrativeGlobalParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity


=end text

=back



=head2 UnshareNarrativeGlobalParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
wsi has a value which is a DashboardService.WorkspaceIdentity


=end text

=back



=cut

package DashboardService::DashboardServiceClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
