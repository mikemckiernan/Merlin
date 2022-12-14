# About Merlin

NVIDIA Merlin is an open source library that accelerates recommender
systems on NVIDIA GPUs.
The library brings together several component libraries that simplifies
the process of building high-performing recommenders at scale.

## Key Parts of a Recommender System

The following diagram identifies the key parts of a recommender system and the corresponding Merlin libraries.

![Recommender system diagram](../images/recommender-systems-dev-web-850.svg)

::::{grid} 2
:::{grid-item-card} ETL
The NVTabular library is designed to provide GPU-accelerated feature engineering.

You can develop an ETL workflow that creates a data pipeline for your recommender system.
+++
[NVTabular](https://nvidia-merlin.github.io/dataloader/main/)
:::
:::{grid-item-card} Data Loading

The Merlin Dataloader provides GPU-accelerated data loading.

+++
[Dataloader](https://nvidia-merlin.github.io/dataloader/main/)
:::
::::

::::{grid} 2
:::{grid-item-card} Training

Merlin Models provides classic models and a building-block design that enables you to build your own modeling architecture.

Transformer4Rec excels for developing session-based recommender models.

Merlin HugeCTR supports training and inference of large deep learning models and can spread the workload across multiple GPUs and hosts.
+++
[Models](https://nvidia-merlin.github.io/models/main/) |
[Transformers4Rec](https://nvidia-merlin.github.io/Transformers4Rec/main/) |
[HugeCTR](https://nvidia-merlin.github.io/HugeCTR/main/)
:::
:::{grid-item-card} Inference

The Merlin Systems library simplifies deploying your recommender model into production with Triton Inference Server.

The library enables you to leverage your feature engineering workflow from NVTabular to create a serving ensemble.
+++
[Systems](https://nvidia-merlin.github.io/systems/main/)
:::
::::

## Related Resources

Merlin GitHub Repository
: <https://github.com/NVIDIA-Merlin/Merlin>

Developer website for Merlin
: More information about Merlin is available at our developer website:
  <https://developer.nvidia.com/nvidia-merlin>