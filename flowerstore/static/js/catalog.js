document.addEventListener("DOMContentLoaded", function () {
    const video = document.querySelector(".hero-video");
    if (video) {
        const tryPlay = () => {
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(() => {
                    video.setAttribute("controls", "controls");
                    video.classList.add("hero-video--controls");
                });
            }
        };

        if (video.readyState >= 2) {
            tryPlay();
        } else {
            video.addEventListener("loadeddata", tryPlay, { once: true });
        }
    }

    const filterToggle = document.querySelector("[data-filter-toggle]");
    const filterModal = document.querySelector("[data-filter-modal]");
    const closeTriggers = document.querySelectorAll("[data-filter-close]");
    const choiceGroups = document.querySelectorAll("[data-choice-group]");
    const filterForm = document.getElementById("catalog-form");
    const filterChips = document.querySelectorAll("[data-chip-clear]");
    const sortDisplay = document.querySelector("[data-sort-display]");
    const sortSelects = document.querySelectorAll('select[name="sort_order"]');

    const escapeValue = (value) => {
        if (window.CSS && CSS.escape) {
            return CSS.escape(value);
        }
        return value.replace(/["\\]/g, "\\$&");
    };

    const syncSortInputs = (value, sourceSelect) => {
        if (!sortSelects.length) return;
        sortSelects.forEach((selectEl) => {
            if (sourceSelect && selectEl === sourceSelect) return;
            selectEl.value = value;
        });
    };

    const updateSortDisplay = () => {
        if (!sortDisplay || !sortSelects.length) return;
        const primarySelect = sortSelects[0];
        const currentValue = primarySelect.value;
        if (!currentValue) {
            sortDisplay.textContent = sortDisplay.dataset.placeholder || "";
            sortDisplay.classList.add("is-muted");
            return;
        }
        const optionSelector = `option[value="${escapeValue(currentValue)}"]`;
        const option = primarySelect.querySelector(optionSelector);
        const label = option ? option.textContent.trim() : "";
        sortDisplay.textContent = label || (sortDisplay.dataset.placeholder || "");
        if (label) {
            sortDisplay.classList.remove("is-muted");
        } else {
            sortDisplay.classList.add("is-muted");
        }
    };

    if (filterToggle && filterModal) {
        const openModal = () => {
            filterModal.classList.add("is-open");
            document.body.style.overflow = "hidden";
        };

        const closeModal = () => {
            filterModal.classList.remove("is-open");
            document.body.style.overflow = "";
        };

        filterToggle.addEventListener("click", openModal);
        closeTriggers.forEach((btn) => btn.addEventListener("click", closeModal));
        filterModal.addEventListener("click", (event) => {
            if (event.target === filterModal) {
                closeModal();
            }
        });
    }

    choiceGroups.forEach((group) => {
        const toggleBtn = group.querySelector("[data-choice-toggle]");
        const list = group.querySelector("[data-choice-list]");
        const optionButtons = list ? list.querySelectorAll("[data-choice-value]") : [];
        const select = group.querySelector("select");
        const isSortGroup = group.dataset.choiceType === "sort";
        const isAutoSubmit = group.hasAttribute("data-auto-submit");
        if (!toggleBtn || !list || !select || !optionButtons.length) return;

        const setActiveOption = (value) => {
            optionButtons.forEach((btn) => {
                btn.classList.toggle("is-active", btn.dataset.choiceValue === value);
            });
            if (isSortGroup) {
                updateSortDisplay();
            }
        };

        const closeList = () => {
            group.classList.remove("is-open");
            toggleBtn.setAttribute("aria-expanded", "false");
            list.setAttribute("aria-hidden", "true");
        };

        const openList = () => {
            group.classList.add("is-open");
            toggleBtn.setAttribute("aria-expanded", "true");
            list.setAttribute("aria-hidden", "false");
        };

        toggleBtn.addEventListener("click", (event) => {
            event.stopPropagation();
            if (group.classList.contains("is-open")) {
                closeList();
            } else {
                openList();
            }
        });

        optionButtons.forEach((btn) => {
            btn.addEventListener("click", (event) => {
                event.preventDefault();
                event.stopPropagation();
                const selectedValue = btn.dataset.choiceValue;
                if (select.value !== selectedValue) {
                    select.value = selectedValue;
                    select.dispatchEvent(new Event("change", { bubbles: true }));
                }
                setActiveOption(selectedValue);
                if (isSortGroup) {
                    syncSortInputs(selectedValue, select);
                    updateSortDisplay();
                    if (isAutoSubmit && filterForm) {
                        if (typeof filterForm.requestSubmit === "function") {
                            filterForm.requestSubmit();
                        } else {
                            filterForm.submit();
                        }
                    }
                }
            });
        });

        group.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeList();
                toggleBtn.focus();
            }
        });

        setActiveOption(select.value);
        if (isSortGroup) {
            updateSortDisplay();
        }
    });

    if (sortDisplay && sortSelects.length) {
        updateSortDisplay();
        sortSelects.forEach((select) => select.addEventListener("change", () => {
            syncSortInputs(select.value, select);
            updateSortDisplay();
        }));
    }

    if (filterForm && filterChips.length) {
        filterChips.forEach((chip) => {
            chip.addEventListener("click", () => {
                const targetField = chip.dataset.chipClear;
                if (!targetField) return;

                if (targetField === "filter_category") {
                    const select = filterForm.querySelector('[name="filter_category"]');
                    if (select) {
                        select.value = "";
                    }
                }

                if (targetField === "available") {
                    const checkbox = filterForm.querySelector('[name="available"]');
                    if (checkbox) {
                        checkbox.checked = false;
                    }
                }

                if (targetField === "sort_order") {
                    const sortFields = filterForm.querySelectorAll('[name="sort_order"]');
                    sortFields.forEach((field) => {
                        field.value = "";
                        field.dispatchEvent(new Event("change", { bubbles: true }));
                    });
                }

                filterForm.submit();
            });
        });
    }
});
