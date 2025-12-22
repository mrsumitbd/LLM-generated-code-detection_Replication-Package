from functools import cached_property

class GPUDropletsResourceWithStreamingResponse:
    def __init__(self, gpu_droplets: GPUDropletsResource) -> None:
        self._client = gpu_droplets

    @cached_property
    def backups(self) -> BackupsResourceWithStreamingResponse:
        return BackupsResourceWithStreamingResponse(self._client.backups)

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._client.actions)

    @cached_property
    def destroy_with_associated_resources(self) -> DestroyWithAssociatedResourcesResourceWithStreamingResponse:
        return DestroyWithAssociatedResourcesResourceWithStreamingResponse(
            self._client.destroy_with_associated_resources
        )

    @cached_property
    def autoscale(self) -> AutoscaleResourceWithStreamingResponse:
        return AutoscaleResourceWithStreamingResponse(self._client.autoscale)

    @cached_property
    def firewalls(self) -> FirewallsResourceWithStreamingResponse:
        return FirewallsResourceWithStreamingResponse(self._client.firewalls)

    @cached_property
    def floating_ips(self) -> FloatingIPsResourceWithStreamingResponse:
        return FloatingIPsResourceWithStreamingResponse(self._client.floating_ips)

    @cached_property
    def images(self) -> ImagesResourceWithStreamingResponse:
        return ImagesResourceWithStreamingResponse(self._client.images)

    @cached_property
    def load_balancers(self) -> LoadBalancersResourceWithStreamingResponse:
        return LoadBalancersResourceWithStreamingResponse(self._client.load_balancers)

    @cached_property
    def sizes(self) -> SizesResourceWithStreamingResponse:
        return SizesResourceWithStreamingResponse(self._client.sizes)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithStreamingResponse:
        return SnapshotsResourceWithStreamingResponse(self._client.snapshots)

    @cached_property
    def volumes(self) -> VolumesResourceWithStreamingResponse:
        return VolumesResourceWithStreamingResponse(self._client.volumes)

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse(self._client.account)