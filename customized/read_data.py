import os
import xarray as xr


def load_xarray_h5(file_path: str, engine_order: list[str] | None = None, load_into_memory: bool = True) -> "xr.Dataset":
    """
    Load an xarray.Dataset stored in an HDF5 (.h5) file.

    Parameters
    ----------
    file_path : str
        Path to the .h5 file.
    group : str | None
        HDF5 group name where the dataset is stored (if any).
    engine_order : list[str] | None
        List of xarray engines to try (default: ["h5netcdf", "netcdf4"]).
    load_into_memory : bool
        If True, call .load() on the returned dataset to read it into memory.

    Returns
    -------
    xr.Dataset
        The loaded xarray Dataset.

    Raises
    ------
    FileNotFoundError
        If file_path does not exist.
    RuntimeError
        If the file cannot be opened as an xarray Dataset with the tried engines.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")

    engines = engine_order or ["h5netcdf", "netcdf4"]
    last_exc = None
    for eng in engines:
        try:
            ds = xr.open_dataset(file_path, engine=eng)
            if load_into_memory:
                ds = ds.load()
            return ds
        except Exception as exc:
            last_exc = exc

    # Final fallback: let xarray choose the engine
    try:
        ds = xr.open_dataset(file_path)
        if load_into_memory:
            ds = ds.load()
        return ds
    except Exception as exc:
        raise RuntimeError(f"Failed to open '{file_path}' as an xarray Dataset. Tried engines {engines}. Last error: {last_exc}") from exc

if __name__ == "__main__":
    from customized.read_data import load_xarray_h5
    ds = load_xarray_h5(r"data/QPU_project/2025-08-26/#941_LCH_CZ_conditional_phase_120536/ds_raw.h5")
    print(ds)
