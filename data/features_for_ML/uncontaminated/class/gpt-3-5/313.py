from functools import cached_property

class GPUDropletsResourceWithStreamingResponse:

    def __init__(self, gpu_droplets: GPUDropletsResource) -> None:
        self.gpu_droplets = gpu_droplets

    @cached_property
    def backups(self) -> BackupsResourceWithStreamingResponse:
        return BackupsResourceWithStreamingResponse()

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse()

    @cached_property
    def destroy_with_associated_resources(self) -> DestroyWithAssociatedResourcesResourceWithStreamingResponse:
        return DestroyWithAssociatedResourcesResourceWithStreamingResponse()

    @cached_property
    def autoscale(self) -> AutoscaleResourceWithStreamingResponse:
        return AutoscaleResourceWithStreamingResponse()

    @cached_property
    def firewalls(self) -> FirewallsResourceWithStreamingResponse:
        return FirewallsResourceWithStreamingResponse()

    @cached_property
    def floating_ips(self) -> FloatingIPsResourceWithStreamingResponse:
        return FloatingIPsResourceWithStreamingResponse()

    @cached_property
    def images(self) -> ImagesResourceWithStreamingResponse:
        return ImagesResourceWithStreamingResponse()

    @cached_property
    def load_balancers(self) -> LoadBalancersResourceWithStreamingResponse:
        return LoadBalancersResourceWithStreamingResponse()

    @cached_property
    def sizes(self) -> SizesResourceWithStreamingResponse:
        return SizesResourceWithStreamingResponse()

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithStreamingResponse:
        return SnapshotsResourceWithStreamingResponse()

    @cached_property
    def volumes(self) -> VolumesResourceWithStreamingResponse:
        return VolumesResourceWithStreamingResponse()

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse()