!program optimise_fortran
!    implicit none
!
!    integer, parameter :: sp = selected_real_kind(p=8)
!    real(sp), dimension(2) :: radii
!    real(sp), dimension(2, 2) :: initial_centres, final_centres
!    integer :: n_steps, n_bubbles, i, j, rep_const
!    real(sp) :: learning_rate
!
!    radii = (/1, 1 /)
!    initial_centres(1,1) = -3
!    initial_centres(1,2) = 0
!    initial_centres(2,1) = 3
!    initial_centres(2,2) = 0
!    n_steps = 1000
!    n_bubbles = 2
!    rep_const = 600
!    learning_rate = 0.01
!
!    call optimise_pos(n_bubbles, radii, initial_centres, n_steps, learning_rate, rep_const, final_centres)
!
!    do i =1,n_bubbles
!        do j = 1, 2
!            print *, final_centres(i,j)
!        end do
!    end do
!
!end program optimise_fortran

subroutine optimise_pos(n_bubbles, radii, centres_in, n_steps, learning_rate, rep_const, centres_out)

    implicit none

    integer, parameter :: sp = selected_real_kind(p=8)
    integer, intent(in) :: n_steps, n_bubbles, rep_const
    real(sp), dimension(n_bubbles), intent(in) :: radii
    real(sp), dimension(n_bubbles, 2), intent(in) :: centres_in
    real(sp), dimension(n_bubbles, 2), intent(out) :: centres_out
    real(sp), intent(in) :: learning_rate

    real(sp), dimension(n_bubbles, 2) :: forces
    integer :: i

    call get_forces(n_bubbles, radii, centres_in, rep_const, forces)

    ! Start optimisation
    centres_out = centres_in

    do i = 1, n_steps
        call update_positions(n_bubbles, centres_out, forces, learning_rate)
        call get_forces(n_bubbles, radii, centres_out, rep_const, forces)
    end do

end subroutine optimise_pos


subroutine get_forces(n_bubbles, radii, centres_in, rep_const, forces)
    implicit none

    integer, parameter :: sp = selected_real_kind(p=8)
    integer, intent(in) :: n_bubbles, rep_const
    real(sp), dimension(n_bubbles), intent(in) :: radii
    real(sp), dimension(n_bubbles, 2), intent(in) :: centres_in
    real(sp), dimension(n_bubbles, 2), intent(out) :: forces

    integer :: i, j
    real(sp), dimension(2) :: dist_vec
    real(sp) :: norm, force_mag

    ! Initialise the forces to zero
    do i = 1, n_bubbles
        forces(i,:) = 0
    end do

    do i = 1, n_bubbles-1
        do j = i+1, n_bubbles
            dist_vec = centres_in(j,:) - centres_in(i,:)
            norm = sqrt(dot_product(dist_vec, dist_vec))

            dist_vec = dist_vec/norm
            call get_force_magnitude(radii(i), radii(j), centres_in(i,:),  centres_in(j,:), rep_const, force_mag)

            forces(i,:) = forces(i,:) - dist_vec * force_mag
            forces(j,:) = forces(j,:) + dist_vec * force_mag

        end do
    end do

end subroutine get_forces

subroutine get_force_magnitude(r1, r2, c1, c2, rep_const, force_mag)
    implicit none

    integer, parameter :: sp = selected_real_kind(p=8)
    real(sp), intent(in) :: r1, r2
    real(sp), dimension(2), intent(in) :: c1, c2
    real(sp), intent(out) :: force_mag
    integer, intent(in) :: rep_const

    real(sp), dimension(2) :: dist_vec
    real(sp) :: dist

    dist_vec = c2 - c1
    dist = sqrt(dot_product(dist_vec, dist_vec))-r1-r2

    if (dist < 0) then
        force_mag = rep_const*dist
    else 
        force_mag = 2*dist
    end if

end subroutine get_force_magnitude

subroutine update_positions(n_bubbles, current_positions, current_forces, learning_rate)
    implicit none

    integer, parameter :: sp = selected_real_kind(p=8)
    integer, intent(in) :: n_bubbles
    real(sp), dimension(n_bubbles, 2), intent(inout) :: current_positions
    real(sp), dimension(n_bubbles, 2), intent(in) :: current_forces
    real(sp), intent(in) :: learning_rate

    current_positions = current_positions - learning_rate * current_forces

end subroutine update_positions