from .sizes import (
    SizesResource,
    AsyncSizesResource,
    SizesResourceWithRawResponse,
    AsyncSizesResourceWithRawResponse,
    SizesResourceWithStreamingResponse,
    AsyncSizesResourceWithStreamingResponse,
)
from .volumes.volumes import (
    VolumesResource,
    AsyncVolumesResource,
    VolumesResourceWithRawResponse,
    AsyncVolumesResourceWithRawResponse,
    VolumesResourceWithStreamingResponse,
    AsyncVolumesResourceWithStreamingResponse,
)
from .load_balancers.load_balancers import (
    LoadBalancersResource,
    AsyncLoadBalancersResource,
    LoadBalancersResourceWithRawResponse,
    AsyncLoadBalancersResourceWithRawResponse,
    LoadBalancersResourceWithStreamingResponse,
    AsyncLoadBalancersResourceWithStreamingResponse,
)
from .backups import (
    BackupsResource,
    AsyncBackupsResource,
    BackupsResourceWithRawResponse,
    AsyncBackupsResourceWithRawResponse,
    BackupsResourceWithStreamingResponse,
    AsyncBackupsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .firewalls.firewalls import (
    FirewallsResource,
    AsyncFirewallsResource,
    FirewallsResourceWithRawResponse,
    AsyncFirewallsResourceWithRawResponse,
    FirewallsResourceWithStreamingResponse,
    AsyncFirewallsResourceWithStreamingResponse,
)
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .account.account import (
    AccountResource,
    AsyncAccountResource,
    AccountResourceWithRawResponse,
    AsyncAccountResourceWithRawResponse,
    AccountResourceWithStreamingResponse,
    AsyncAccountResourceWithStreamingResponse,
)
from .floating_ips.floating_ips import (
    FloatingIPsResource,
    AsyncFloatingIPsResource,
    FloatingIPsResourceWithRawResponse,
    AsyncFloatingIPsResourceWithRawResponse,
    FloatingIPsResourceWithStreamingResponse,
    AsyncFloatingIPsResourceWithStreamingResponse,
)
from .actions import (
    ActionsResource,
    AsyncActionsResource,
    ActionsResourceWithRawResponse,
    AsyncActionsResourceWithRawResponse,
    ActionsResourceWithStreamingResponse,
    AsyncActionsResourceWithStreamingResponse,
)
from .autoscale import (
    AutoscaleResource,
    AsyncAutoscaleResource,
    AutoscaleResourceWithRawResponse,
    AsyncAutoscaleResourceWithRawResponse,
    AutoscaleResourceWithStreamingResponse,
    AsyncAutoscaleResourceWithStreamingResponse,
)
from .snapshots import (
    SnapshotsResource,
    AsyncSnapshotsResource,
    SnapshotsResourceWithRawResponse,
    AsyncSnapshotsResourceWithRawResponse,
    SnapshotsResourceWithStreamingResponse,
    AsyncSnapshotsResourceWithStreamingResponse,
)
from .images.images import (
    ImagesResource,
    AsyncImagesResource,
    ImagesResourceWithRawResponse,
    AsyncImagesResourceWithRawResponse,
    ImagesResourceWithStreamingResponse,
    AsyncImagesResourceWithStreamingResponse,
)
from .destroy_with_associated_resources import (
    DestroyWithAssociatedResourcesResource,
    AsyncDestroyWithAssociatedResourcesResource,
    DestroyWithAssociatedResourcesResourceWithRawResponse,
    AsyncDestroyWithAssociatedResourcesResourceWithRawResponse,
    DestroyWithAssociatedResourcesResourceWithStreamingResponse,
    AsyncDestroyWithAssociatedResourcesResourceWithStreamingResponse,
)

class GPUDropletsResourceWithStreamingResponse:
    def __init__(self, gpu_droplets: GPUDropletsResource) -> None:
        self._gpu_droplets = gpu_droplets

        self.create = to_streamed_response_wrapper(
            gpu_droplets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            gpu_droplets.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            gpu_droplets.list,
        )
        self.delete = to_streamed_response_wrapper(
            gpu_droplets.delete,
        )
        self.delete_by_tag = to_streamed_response_wrapper(
            gpu_droplets.delete_by_tag,
        )
        self.list_firewalls = to_streamed_response_wrapper(
            gpu_droplets.list_firewalls,
        )
        self.list_kernels = to_streamed_response_wrapper(
            gpu_droplets.list_kernels,
        )
        self.list_neighbors = to_streamed_response_wrapper(
            gpu_droplets.list_neighbors,
        )
        self.list_snapshots = to_streamed_response_wrapper(
            gpu_droplets.list_snapshots,
        )

    @cached_property
    def backups(self) -> BackupsResourceWithStreamingResponse:
        return BackupsResourceWithStreamingResponse(self._gpu_droplets.backups)

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._gpu_droplets.actions)

    @cached_property
    def destroy_with_associated_resources(self) -> DestroyWithAssociatedResourcesResourceWithStreamingResponse:
        return DestroyWithAssociatedResourcesResourceWithStreamingResponse(
            self._gpu_droplets.destroy_with_associated_resources
        )

    @cached_property
    def autoscale(self) -> AutoscaleResourceWithStreamingResponse:
        return AutoscaleResourceWithStreamingResponse(self._gpu_droplets.autoscale)

    @cached_property
    def firewalls(self) -> FirewallsResourceWithStreamingResponse:
        return FirewallsResourceWithStreamingResponse(self._gpu_droplets.firewalls)

    @cached_property
    def floating_ips(self) -> FloatingIPsResourceWithStreamingResponse:
        return FloatingIPsResourceWithStreamingResponse(self._gpu_droplets.floating_ips)

    @cached_property
    def images(self) -> ImagesResourceWithStreamingResponse:
        return ImagesResourceWithStreamingResponse(self._gpu_droplets.images)

    @cached_property
    def load_balancers(self) -> LoadBalancersResourceWithStreamingResponse:
        return LoadBalancersResourceWithStreamingResponse(self._gpu_droplets.load_balancers)

    @cached_property
    def sizes(self) -> SizesResourceWithStreamingResponse:
        return SizesResourceWithStreamingResponse(self._gpu_droplets.sizes)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithStreamingResponse:
        return SnapshotsResourceWithStreamingResponse(self._gpu_droplets.snapshots)

    @cached_property
    def volumes(self) -> VolumesResourceWithStreamingResponse:
        return VolumesResourceWithStreamingResponse(self._gpu_droplets.volumes)

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse(self._gpu_droplets.account)