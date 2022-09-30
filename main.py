#!/usr/bin/env python

import os

from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, Token
from imports.azurerm import AzurermProvider, ResourceGroup, VirtualNetwork
from imports.terraform_azure_yugabyte import TerraformAzureYugabyte


class MyStack(TerraformStack):
  def __init__(self, scope: Construct, ns: str):
    super().__init__(scope, ns)

    # define resources here
    # TODO change these
    location="Southeast Asia"
    address_space=["10.12.0.0/27"]
    resource_group_name="yugabyte-cdktf"
    tag = {
      "ENV": "Dev",
      "PROJECT": "AZ_TF.Yugabyte"
    }
    features = {}

    # AzurermProvider(self, "Azurerm",
    #   features=features
    # )
    # resource_group = ResourceGroup(self, 'yugabyte-rg',
    #   name=resource_group_name,
    #   location = location,
    #   tags = tag
    #   )
    # example_vnet = VirtualNetwork(self, 'example_vnet',
    #   depends_on =[resource_group],
    #   name="example_vnet",
    #   location=location,
    #   address_space=address_space,
    #   resource_group_name=Token().as_string(resource_group.name),
    #   tags = tag
    #   )



    yugabyte_cluster = TerraformAzureYugabyte(self, "yugabyte-cluster", 
      cluster_name = "test-cluster",
      ssh_private_key = os.environ["PATH_TO_SSH_PRIVATE_KEY_FILE"],
      ssh_public_key  = os.environ["PATH_TO_SSH_PUBLIC_KEY_FILE"],
      # in yugabyte module, this also gets set as vm username (which makes sense), but that means it cannot be anything that Azure doesn't allow, including root, admin, etc
      # see https://github.com/Azure/azure-cli/issues/582
      ssh_user        = "yugabyte",
      # The region name where the nodes should be spawned.
      region_name = location,
      # The name of resource group in which all Azure resource will be created.
      resource_group = Token().as_string(resource_group_name),
      # Replication factor.
      replication_factor = "3",
      # The number of nodes in the cluster, this cannot be lower than the replication factor.
      node_count = "3"
    )

    TerraformOutput(self, 'vnet_id',
      #value=example_vnet.id
      value=yugabyte_cluster.cluster_name
      )

app = App()
MyStack(app, "cdktf-azure-demo")

app.synth()
